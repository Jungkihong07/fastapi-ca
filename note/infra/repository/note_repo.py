from fastapi import HTTPException
from database import SessionLocal
from sqlalchemy.orm import joinedload
from note.domain.note import Note as NoteVO
from note.domain.repository.note_repo import INoteRepository
from note.infra.db_models.note import Note, Tag
from utils.db_utils import row_to_dict


class NoteRepository(INoteRepository):
    def get_notes(
        self,
        user_id: str,
        page: int,
        item_per_page: int,
    ) -> tuple[int, list[NoteVO]]:
        with SessionLocal() as db:
            query = (
                db.query(Note)
                .options(
                    joinedload(Note.tags)
                )  # joinedload 함수를 이용하여 조회할 때, 연관테이블의 데이터를 함께 가져온다.
                .filter(Note.user_id == user_id)
            )

            total_count = query.count()
            notes = query.offset((page - 1) * item_per_page).limit(item_per_page).all()

        note_vos = [NoteVO(**row_to_dict(note)) for note in notes]

        return total_count, note_vos

    def find_by_id(self, user_id, id: str) -> NoteVO:
        with SessionLocal() as db:
            note = (
                db.query(Note)
                .options(joinedload(Note.tags))
                .filter(Note.user_id == user_id, Note.id == id)
                .first()
            )
            if not note:
                raise HTTPException(status_code=422)
        return NoteVO(**row_to_dict(note))

    def save(self, user_id: str, note_vo: NoteVO) -> NoteVO:
        with SessionLocal() as db:
            tags: list[Tag] = []
            for tag in note_vo.tags:
                existing_tag = db.query(Tag).filter(Tag.name == tag.name).first()
                if existing_tag:
                    tags.append(existing_tag)
                else:
                    tags.append(
                        Tag(
                            id=tag.id,
                            name=tag.name,
                            created_at=tag.created_at,
                            updated_at=tag.updated_at,
                        )
                    )
        new_note = Note(
            id=note_vo.id,
            user_id=user_id,
            title=note_vo.title,
            content=note_vo.content,
            memo_date=note_vo.memo_date,
            tags=tags,
            created_at=note_vo.created_at,
            updated_at=note_vo.updated_at,
        )

        db.add(new_note)
        db.commit()

    def update(self, user_id: str, note_vo: NoteVO) -> NoteVO:
        with SessionLocal() as db:
            self.delete_tags(user_id, note_vo.id)

            note = (
                db.query(Note)
                .filter(Note.user_id == user_id, Note.id == note_vo.id)
                .first()
            )

            if not note:
                raise HTTPException(status_code=422)

            note.title = note_vo.title
            note.content = note_vo.content
            note.memo_date = note_vo.memo_date

            tags: list[Tag] = []
            for tag in note_vo.tags:
                existing_tag = db.query(Tag).filter(Tag.name == tag.name).first()
                if existing_tag:
                    tags.append(existing_tag)
                else:
                    tags.append(
                        Tag(
                            id=tag.id,
                            name=tag.name,
                            created_at=tag.created_at,
                            updated_at=tag.updated_at,
                        )
                    )

            note.tags = tags

            db.add(note)
            db.commit()

            return NoteVO(**row_to_dict(note))

    def delete(self, user_id: str, id: str):
        with SessionLocal() as db:
            self.delete_tags(user_id, id)

            note = db.query(Note).filter(Note.user_id == user_id, Note.id == id).first()
            if not note:
                raise HTTPException(status_code=422)

            db.delete(note)
            db.commit()

    def delete_tags(self, user_id: str, id: str):
        with SessionLocal() as db:
            note = db.query(Note).filter(Note.user_id == user_id, Note.id == id).first()
            if not note:
                raise HTTPException(status_code=422)

            note.tags = []
            db.add(note)
            db.commit()

            # 노트의 태그를 삭제하고 나서 고아가 된(노트에 연결돼 있지 않은) 태그를 찾아서 삭제한다.
            unused_tags = db.query(Tag).filter(~Tag.notes.any()).all()
            for tag in unused_tags:
                db.delete(tag)

            db.commit()

    def get_notes_by_tag_name(
        self,
        user_id: str,
        tag_name: str,
        page: int,
        items_per_page: int,
    ) -> tuple[int, list[NoteVO]]:
        with SessionLocal() as db:
            tag = db.query(Tag).filter_by(name=tag_name).first()

            if not tag:
                return 0, []

            query = (
                db.query(Note)
                # .options(joinedload(Note.tags))
                .filter(
                    Note.user_id == user_id,
                    Note.tags.any(id=tag.id),
                )
            )

            total_count = query.count()
            notes = (
                query.offset((page - 1) * items_per_page).limit(items_per_page).all()
            )

        note_vos = [NoteVO(**row_to_dict(note)) for note in notes]

        return total_count, note_vos
