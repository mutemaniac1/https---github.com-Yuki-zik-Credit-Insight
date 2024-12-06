# crud/overdue_aging_analysis.py
# -*- coding: utf-8 -*-
from sqlalchemy.orm import Session
from database.models.overdue_aging_analysis import OverdueAgingAnalysis

class OverdueAgingAnalysisCRUD:
    def create_overdue_aging(self, db: Session, aging_data: dict):
        """
        创建新的逾期账龄分析记录
        """
        new_aging = OverdueAgingAnalysis(**aging_data)
        db.add(new_aging)
        db.commit()
        db.refresh(new_aging)
        return new_aging

    def get_overdue_aging_by_id(self, db: Session, aging_id: int):
        """
        根据账龄ID获取逾期账龄分析
        """
        return db.query(OverdueAgingAnalysis).filter(OverdueAgingAnalysis.aging_id == aging_id).first()

    def get_overdue_agings_by_status(self, db: Session, status_id: int):
        """
        获取某个财务状态的所有逾期账龄分析记录
        """
        return db.query(OverdueAgingAnalysis).filter(OverdueAgingAnalysis.status_id == status_id).all()

    def update_overdue_aging(self, db: Session, aging_id: int, update_data: dict):
        """
        更新逾期账龄分析信息
        """
        aging = db.query(OverdueAgingAnalysis).filter(OverdueAgingAnalysis.aging_id == aging_id).first()
        if aging:
            for key, value in update_data.items():
                setattr(aging, key, value)
            db.commit()
            db.refresh(aging)
        return aging

    def delete_overdue_aging(self, db: Session, aging_id: int):
        """
        删除逾期账龄分析记录
        """
        aging = db.query(OverdueAgingAnalysis).filter(OverdueAgingAnalysis.aging_id == aging_id).first()
        if aging:
            db.delete(aging)
            db.commit()
        return aging

# 实例化 OverdueAgingAnalysisCRUD
overdue_aging_analysis_crud = OverdueAgingAnalysisCRUD()
