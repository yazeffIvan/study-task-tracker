from pydantic import BaseModel, Field


class CourseCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200, strip_whitespace=True)


class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200, strip_whitespace=True)
    deadline: str | None = None
