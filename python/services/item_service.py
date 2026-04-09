from typing import List, Optional, Tuple
from repositories.item_repository import ItemRepository


class ItemService:
    def __init__(self, repository: ItemRepository):
        self.repository = repository

    def get_all_items(self) -> List[Tuple]:
        return self.repository.get_all_items()

    def get_item(self, item_id: int) -> Optional[Tuple]:
        return self.repository.get_item_by_id(item_id)

    def create_item(self, title: str, description: str) -> int:
        if not title or len(title.strip()) == 0:
            raise ValueError("Title cannot be empty")
        return self.repository.create_item(title, description)

    def update_item(self, item_id: int, title: str, description: str) -> bool:
        if not title or len(title.strip()) == 0:
            raise ValueError("Title cannot be empty")
        return self.repository.update_item(item_id, title, description)

    def delete_item(self, item_id: int) -> bool:
        return self.repository.delete_item(item_id)
