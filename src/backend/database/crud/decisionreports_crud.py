# crud/decision_report.py
# -*- coding: utf-8 -*-
from sqlalchemy.orm import Session
from database.models.decision_report import DecisionReport

class DecisionReportCRUD:
    def create_decision_report(self, db: Session, report_data: dict):
        """
        创建新的决策报告
        """
        new_report = DecisionReport(**report_data)
        db.add(new_report)
        db.commit()
        db.refresh(new_report)
        return new_report

    def get_decision_report_by_id(self, db: Session, decision_report_id: int):
        """
        根据报告ID获取决策报告
        """
        return db.query(DecisionReport).filter(DecisionReport.decision_report_id == decision_report_id).first()

    def get_decision_reports_by_user(self, db: Session, user_id: int):
        """
        获取某个用户的所有决策报告
        """
        return db.query(DecisionReport).filter(DecisionReport.user_id == user_id).all()

    def get_decision_reports_by_enterprise(self, db: Session, enterprise_id: int):
        """
        获取某个企业的所有决策报告
        """
        return db.query(DecisionReport).filter(DecisionReport.enterprise_id == enterprise_id).all()

    def update_decision_report(self, db: Session, decision_report_id: int, update_data: dict):
        """
        更新决策报告信息
        """
        report = db.query(DecisionReport).filter(DecisionReport.decision_report_id == decision_report_id).first()
        if report:
            for key, value in update_data.items():
                setattr(report, key, value)
            db.commit()
            db.refresh(report)
        return report

    def delete_decision_report(self, db: Session, decision_report_id: int):
        """
        删除决策报告
        """
        report = db.query(DecisionReport).filter(DecisionReport.decision_report_id == decision_report_id).first()
        if report:
            db.delete(report)
            db.commit()
        return report

# 实例化 DecisionReportCRUD
decision_report_crud = DecisionReportCRUD()
