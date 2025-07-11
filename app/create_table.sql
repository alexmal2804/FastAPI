 create table if not exists users (
  id serial primary key,
  name text not null,
  password text not null
 )
  
'''
class Todo (BaseModel):
    title: Annotated[str, Field(min_length=3, max_length=50)] 
    description: Annotated[str, Field(min_length=10, max_length=200)] 
    completed: bool = False
'''
create table if not exists todos (
  id serial primary key,
  title text not null,
  description text,
  completed boolean default false
);

ALTER TABLE todos ADD COLUMN user_id INTEGER REFERENCES users(id) ON DELETE CASCADE;
