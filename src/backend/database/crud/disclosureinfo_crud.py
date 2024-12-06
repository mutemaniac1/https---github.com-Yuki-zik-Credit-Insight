# crud/disclosure_info.py
# -*- coding: utf-8 -*-
from sqlalchemy.orm import Session
from database.models.disclosure_info import DisclosureInfo

class DisclosureInfoCRUD:
    def create_disclosure_info(self, db: Session, info_data: dict):
        """
        创建新的披露信息
        """
        new_info = DisclosureInfo(**info_data)
        db.add(new_info)
        db.commit()
        db.refresh(new_info)
        return new_info

    def get_disclosure_info_by_id(self, db: Session, disclosure_id: int):
        """
        根据披露ID获取信息
        """
        return db.query(DisclosureInfo).filter(DisclosureInfo.disclosure_id == disclosure_id).first()

    def get_disclosure_infos_by_enterprise(self, db: Session, enterprise_id: int):
        """
        获取某个企业的所有披露信息
        """
        return db.query(DisclosureInfo).filter(DisclosureInfo.enterprise_id == enterprise_id).all()

    def update_disclosure_info(self, db: Session, disclosure_id: int, update_data: dict):
        """
        更新披露信息
        """
        info = db.query(DisclosureInfo).filter(DisclosureInfo.disclosure_id == disclosure_id).first()
        if info:
            for key, value in update_data.items():
                setattr(info, key, value)
            db.commit()
            db.refresh(info)
        return info

    def delete_disclosure_info(self, db: Session, disclosure_id: int):
        """
        删除披露信息
        """
        info = db.query(DisclosureInfo).filter(DisclosureInfo.disclosure_id == disclosure_id).first()
        if info:
            db.delete(info)
            db.commit()
        return info

# 实例化 DisclosureInfoCRUD
disclosure_info_crud = DisclosureInfoCRUD()
