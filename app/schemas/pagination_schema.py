'''
import re
from datetime import datetime
from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel, EmailStr, Field, HttpUrl, validator, conint

# Pagination Model
class Pagination(BaseModel):
    page: int = Field(..., description="Current page number.")
    per_page: int = Field(..., description="Number of items per page.")
    total_items: int = Field(..., description="Total number of items.")
    total_pages: int = Field(..., description="Total number of pages.")

    class Config:
        json_schema_extra = {
            "example": {
                "page": 1,
                "per_page": 10,
                "total_items": 50,
                "total_pages": 5
            }
        }



class PaginationLink(BaseModel):
    rel: str
    href: HttpUrl
    method: str = "GET"

class EnhancedPagination(Pagination):
    links: List[PaginationLink] = []

    def add_link(self, rel: str, href: str):
        self.links.append(PaginationLink(rel=rel, href=href))
'''

import re
from datetime import datetime
from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel, EmailStr, Field, HttpUrl, validator, conint

# Pagination Model
class Pagination(BaseModel):
    page: int = Field(..., description="Current page number.")
    per_page: int = Field(..., description="Number of items per page.")
    total_items: int = Field(..., description="Total number of items.")
    total_pages: int = Field(..., description="Total number of pages.")

    @validator("page")
    def validate_page(cls, v):
        if v < 1:
            raise ValueError("Page must be a positive integer starting from 1.")
        return v

    @validator("per_page")
    def validate_per_page(cls, v):
        if v < 1:
            raise ValueError("Per page must be a positive integer greater than 0.")
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "page": 1,
                "per_page": 10,
                "total_items": 50,
                "total_pages": 5
            }
        }

# Pagination Link Model
class PaginationLink(BaseModel):
    rel: str
    href: HttpUrl
    method: str = "GET"
    additional_metadata: Optional[dict] = None  # Add this line to include additional metadata
    
'''
# Enhanced Pagination with links
class EnhancedPagination(Pagination):
    links: List[PaginationLink] = []

    def add_link(self, rel: str, href: str, method: str = "GET"):
        """Add a navigation link."""
        self.links.append(PaginationLink(rel=rel, href=href, method=method))

    def generate_links(self, base_url: str, skip: int, limit: int, total_items: int) -> None:
        """Generate pagination links (self, first, last, next, prev)."""
        total_pages = (total_items + limit - 1) // limit
        self.add_link("self", f"{base_url}?skip={skip}&limit={limit}")
        self.add_link("first", f"{base_url}?skip=0&limit={limit}")
        self.add_link("last", f"{base_url}?skip={(total_pages - 1) * limit}&limit={limit}")
        
        if skip + limit < total_items:
            self.add_link("next", f"{base_url}?skip={skip + limit}&limit={limit}")

        if skip > 0:
            self.add_link("prev", f"{base_url}?skip={max(skip - limit, 0)}&limit={limit}")
'''
# Enhanced Pagination with links
class EnhancedPagination(Pagination):
    links: List[PaginationLink] = []

    def add_link(self, rel: str, href: str, method: str = "GET", additional_metadata: Optional[dict] = None):
        """Add a navigation link."""
        self.links.append(PaginationLink(rel=rel, href=href, method=method, additional_metadata=additional_metadata))

    def generate_links(self, base_url: str, skip: int, limit: int, total_items: int) -> None:
        """Generate pagination links (self, first, last, next, prev)."""
        total_pages = (total_items + limit - 1) // limit
        self.add_link("self", f"{base_url}?skip={skip}&limit={limit}", additional_metadata={
            "current_page": skip // limit + 1,
            "total_items": total_items,
            "total_pages": total_pages
        })
        self.add_link("first", f"{base_url}?skip=0&limit={limit}", additional_metadata={
            "current_page": 1,
            "total_items": total_items,
            "total_pages": total_pages
        })
        self.add_link("last", f"{base_url}?skip={(total_pages - 1) * limit}&limit={limit}", additional_metadata={
            "current_page": total_pages,
            "total_items": total_items,
            "total_pages": total_pages
        })
        
        if skip + limit < total_items:
            self.add_link("next", f"{base_url}?skip={skip + limit}&limit={limit}", additional_metadata={
                "current_page": (skip + limit) // limit + 1,
                "total_items": total_items,
                "total_pages": total_pages
            })

        if skip > 0:
            self.add_link("prev", f"{base_url}?skip={max(skip - limit, 0)}&limit={limit}", additional_metadata={
                "current_page": (skip - limit) // limit + 1,
                "total_items": total_items,
                "total_pages": total_pages
            })

