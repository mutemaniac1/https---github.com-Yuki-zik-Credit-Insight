# services/overdue_aging_analysis_service.py
# -*- coding: utf-8 -*-
from typing import Optional, List, Dict, Any
from datetime import date
from sqlalchemy.exc import SQLAlchemyError
from backend.database.link import get_session
from backend.database.crud.overdue_aging_analysis_crud import overdue_aging_analysis_crud
from backend.database.models.overdue_aging_analysis import OverdueAgingAnalysis

class OverdueAgingAnalysisService:
    """逾期账龄分析服务类"""
    
    @staticmethod
    async def create_aging_analysis(data: Dict[str, Any]) -> Optional[OverdueAgingAnalysis]:
        """创建逾期账龄分析"""
        try:
            with get_session() as session:
                analysis = overdue_aging_analysis_crud.create(session, data)
                session.commit()
                return analysis
        except SQLAlchemyError as e:
            # 记录日志
            return None
    
    @staticmethod
    async def get_aging_analysis(analysis_id: int) -> Optional[OverdueAgingAnalysis]:
        """获取逾期账龄分析"""
        with get_session() as session:
            return overdue_aging_analysis_crud.get_by_id(session, analysis_id)
    
    @staticmethod
    async def get_financial_status_analyses(
        financial_status_id: int,
        skip: int = 0,
        limit: int = 100
    ) -> List[OverdueAgingAnalysis]:
        """获取财务状态的所有逾期账龄分析"""
        with get_session() as session:
            return overdue_aging_analysis_crud.get_by_financial_status_id(
                session, financial_status_id, skip=skip, limit=limit
            )
    
    @staticmethod
    async def get_latest_financial_status_analysis(
        financial_status_id: int
    ) -> Optional[OverdueAgingAnalysis]:
        """获取财务状态最新的逾期账龄分析"""
        with get_session() as session:
            return overdue_aging_analysis_crud.get_latest_by_financial_status_id(
                session, financial_status_id
            )
    
    @staticmethod
    async def get_aging_analyses(
        skip: int = 0,
        limit: int = 100,
        **filters
    ) -> List[OverdueAgingAnalysis]:
        """获取逾期账龄分析列表"""
        with get_session() as session:
            return overdue_aging_analysis_crud.get_multi(
                session,
                skip=skip,
                limit=limit,
                **filters
            )
    
    @staticmethod
    async def update_aging_analysis(
        analysis_id: int,
        update_data: Dict[str, Any]
    ) -> Optional[OverdueAgingAnalysis]:
        """更新逾期账龄分析"""
        try:
            with get_session() as session:
                analysis = overdue_aging_analysis_crud.get_by_id(session, analysis_id)
                if not analysis:
                    return None
                
                updated_analysis = overdue_aging_analysis_crud.update(
                    session, analysis, update_data
                )
                session.commit()
                return updated_analysis
        except SQLAlchemyError as e:
            # 记录日志
            return None
    
    @staticmethod
    async def delete_aging_analysis(analysis_id: int) -> bool:
        """删除逾期账龄分析"""
        try:
            with get_session() as session:
                analysis = overdue_aging_analysis_crud.get_by_id(session, analysis_id)
                if not analysis:
                    return False
                
                overdue_aging_analysis_crud.delete(session, analysis)
                session.commit()
                return True
        except SQLAlchemyError as e:
            # 记录日志
            return False
    
    @staticmethod
    async def get_analyses_by_date_range(
        financial_status_id: int,
        start_date: date,
        end_date: date
    ) -> List[OverdueAgingAnalysis]:
        """获取指定日期范围内的逾期账龄分析"""
        with get_session() as session:
            return overdue_aging_analysis_crud.get_by_date_range(
                session,
                financial_status_id=financial_status_id,
                start_date=start_date,
                end_date=end_date
            )
    
    @staticmethod
    async def get_analyses_by_aging_period(
        min_days: int = None,
        max_days: int = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[OverdueAgingAnalysis]:
        """获取特定账龄期间的分析记录"""
        with get_session() as session:
            return overdue_aging_analysis_crud.get_by_aging_period(
                session,
                min_days=min_days,
                max_days=max_days,
                skip=skip,
                limit=limit
            )
    
    @staticmethod
    async def get_aging_statistics(
        financial_status_id: int
    ) -> Dict[str, Any]:
        """获取账龄统计信息"""
        with get_session() as session:
            return overdue_aging_analysis_crud.get_aging_statistics(
                session,
                financial_status_id=financial_status_id
            )
    
    @staticmethod
    async def bulk_create_aging_analyses(
        analyses_data: List[Dict[str, Any]]
    ) -> List[OverdueAgingAnalysis]:
        """批量创建逾期账龄分析"""
        created_analyses = []
        try:
            with get_session() as session:
                for data in analyses_data:
                    analysis = overdue_aging_analysis_crud.create(session, data)
                    created_analyses.append(analysis)
                session.commit()
                return created_analyses
        except SQLAlchemyError as e:
            # 记录日志
            return []
    
    @staticmethod
    async def calculate_aging_metrics(
        financial_status_id: int
    ) -> Dict[str, Any]:
        """计算账龄相关指标"""
        with get_session() as session:
            analyses = overdue_aging_analysis_crud.get_by_financial_status_id(
                session, financial_status_id
            )
            
            if not analyses:
                return {
                    'aging_distribution': {},
                    'risk_level': 'low',
                    'trend': 'stable'
                }
            
            # 计算账龄分布
            aging_distribution = {
                '30天以内': 0,
                '31-60天': 0,
                '61-90天': 0,
                '91-180天': 0,
                '180天以上': 0
            }
            
            for analysis in analyses:
                days = analysis.aging_days
                amount = float(analysis.overdue_amount)
                
                if days <= 30:
                    aging_distribution['30天以内'] += amount
                elif days <= 60:
                    aging_distribution['31-60天'] += amount
                elif days <= 90:
                    aging_distribution['61-90天'] += amount
                elif days <= 180:
                    aging_distribution['91-180天'] += amount
                else:
                    aging_distribution['180天以上'] += amount
            
            # 计算风险等级
            total_amount = sum(aging_distribution.values())
            long_term_ratio = (aging_distribution['91-180天'] + aging_distribution['180天以上']) / total_amount if total_amount > 0 else 0
            
            risk_level = 'high' if long_term_ratio > 0.3 else 'medium' if long_term_ratio > 0.1 else 'low'
            
            # 分析趋势
            sorted_analyses = sorted(analyses, key=lambda x: x.aging_date)
            if len(sorted_analyses) >= 2:
                first = sorted_analyses[0].aging_days
                last = sorted_analyses[-1].aging_days
                trend = 'increasing' if last > first else 'decreasing' if last < first else 'stable'
            else:
                trend = 'stable'
            
            return {
                'aging_distribution': aging_distribution,
                'risk_level': risk_level,
                'trend': trend
            }

# 创建服务实例
overdue_aging_analysis_service = OverdueAgingAnalysisService() 
