from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import Session
from sqlalchemy import ForeignKey
# import sqlalchemy  
from sqlalchemy.orm import relationship

class Base(DeclarativeBase):
    pass

class Department(Base):
    __tablename__ = "Departments" 
    ID : Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    Financing : Mapped[int] = mapped_column()
    Name : Mapped[str] = mapped_column()
    teachers: Mapped[list["Teacher"]] = relationship(secondary="Department_Teacher",
        back_populates="departments")
    faculties: Mapped[list["Facultie"]] = relationship(secondary="Department_Facultie",
        back_populates="departments")
    def __repr__(self) -> str:
        return f"Department(ID={self.ID!r}, Financing={self.Financing!r}, Name={self.Name!r})"
    
class Facultie(Base):
    __tablename__ = "Faculties" 
    ID : Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    Dean : Mapped[str] = mapped_column()
    Name : Mapped[str] = mapped_column()
    departments: Mapped[list["Department"]] = relationship(secondary="Department_Facultie",
        back_populates="faculties")
    def __repr__(self) -> str:
        return f"Facultie(ID={self.ID!r}, Dean={self.Dean!r}, Name={self.Name!r})"

class Group(Base):
    __tablename__ = "Groups" 
    ID : Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    Name : Mapped[str] = mapped_column()
    Rating : Mapped[int] = mapped_column()
    Year : Mapped[int] = mapped_column()
    teachers: Mapped[list["Teacher"]] = relationship(secondary="Group_Teacher",
        back_populates="groups")
    def __repr__(self) -> str:
        return f"Group(ID={self.ID!r}, Name={self.Name!r}, Rating={self.Rating!r}, Year={self.Year!r})"
    
class Teacher(Base):
    __tablename__ = "Teachers" 
    ID : Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    FirstName : Mapped[str] = mapped_column()
    LastName : Mapped[str] = mapped_column()
    EmploymentDate : Mapped[str] = mapped_column()
    IsAssistant : Mapped[int] = mapped_column()
    IsProfessor : Mapped[int] = mapped_column()
    Position : Mapped[str] = mapped_column()
    Premium : Mapped[int] = mapped_column()
    Salary : Mapped[int] = mapped_column()
    departments: Mapped[list["Department"]] = relationship(secondary="Department_Teacher",
        back_populates="teachers")
    groups: Mapped[list["Group"]] = relationship(secondary="Group_Teacher",
        back_populates="teachers")
    def __repr__(self) -> str:
        return f"Teacher(ID={self.ID!r}, FirstName={self.FirstName!r}, LastName={self.LastName!r}, EmploymentDate={self.EmploymentDate!r}, IsAssistant={self.IsAssistant!r}, IsProfessor={self.IsProfessor!r}, Position={self.Position!r}, Premium={self.Premium!r}, Salary={self.Salary!r})"

class Department_Teacher(Base):
    __tablename__ = "Department_Teacher"
    ID: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    ID_Department: Mapped[int] = mapped_column(ForeignKey("Departments.ID"))
    ID_Teacher: Mapped[int] = mapped_column(ForeignKey("Teachers.ID"))

class Group_Teacher(Base):
    __tablename__ = "Group_Teacher"
    ID: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    ID_Group: Mapped[int] = mapped_column(ForeignKey("Groups.ID"))
    ID_Teacher: Mapped[int] = mapped_column(ForeignKey("Teachers.ID"))

class Department_Facultie(Base):
    __tablename__ = "Department_Facultie"
    ID: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    ID_Department: Mapped[int] = mapped_column(ForeignKey("Departments.ID"))
    ID_Teacher: Mapped[int] = mapped_column(ForeignKey("Faculties.ID"))

engine = create_engine("sqlite:///db.db")
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

with Session(engine) as session:
    St1 = Department(Financing=10000, Name="Department1")
    St2 = Department(Financing=20000, Name="Department2")
    St3 = Department(Financing=30000, Name="Department3")
    
    St4 = Facultie(Dean="Dean1", Name="Facultie1")
    St5 = Facultie(Dean="Dean2", Name="Computer Science")
    St6 = Facultie(Dean="Dean3", Name="Facultie3")

    St7 = Group(Name="Group1", Rating=1, Year=1)
    St8 = Group(Name="Group2", Rating=2, Year=2)
    St9 = Group(Name="Group3", Rating=3, Year=3)

    St10 = Teacher(FirstName = "Teacher1", LastName = "Teacher1", EmploymentDate = "2015-09-07", IsAssistant = 1, IsProfessor = 0,Position = "Position1", Premium = 100, Salary  = 1000)
    St11 = Teacher(FirstName = "Teacher2", LastName = "Teacher2", EmploymentDate = "2016-09-07", IsAssistant = 0, IsProfessor = 1,Position = "Position2", Premium = 200, Salary  = 2000)
    St12 = Teacher(FirstName = "Teacher3", LastName = "Teacher3", EmploymentDate = "2017-09-07", IsAssistant = 0, IsProfessor = 0,Position = "Position3", Premium = 300, Salary  = 3000)

    session.add_all([St1, St2, St3, St4, St5, St6, St7, St8, St9, St10, St11, St12])
    session.commit()

    St10.departments.append(St1)
    St11.departments.append(St3)
    St12.departments.append(St2)
    St7.teachers.append(St11)
    St8.teachers.append(St10)
    St9.teachers.append(St12)
    St1.faculties.append(St4)
    St1.faculties.append(St6)
    St1.faculties.append(St5)
    session.commit()

# 1. Вывести таблицу кафедр, но расположить ее поля в
# обратном порядке.
    ame = session.query(Department).all()
    print(ame)
    ame.reverse()
    print(ame)

# 2. Вывести названия групп и их рейтинги с уточнением
# имен полей именем таблицы.
    ame = session.query(Group.Name, Group.Rating).all()
    print(ame)
   
# 3. Вывести для преподавателей их фамилию, процент
# ставки по отношению к надбавке и процент ставки
# по отношению к зарплате (сумма ставки и надбавки).
# 4. Вывести таблицу факультетов в виде одного поля в
# следующем формате: “The dean of faculty [faculty] is
# [dean].”.
# 5. Вывести фамилии преподавателей, которые являются
# профессорами и ставка которых превышает 1050.
    ame = session.query(Teacher.LastName).filter(Teacher.IsProfessor == 1).filter(Teacher.Salary > 1050).all()
    print(ame)

# 6. Вывести названия кафедр, фонд финансирования
# которых меньше 11000 или больше 25000.
    ame = session.query(Department.Name).filter(Department.Financing > 11000).filter(Department.Financing < 25000).all()
    print(ame)

# 7. Вывести названия факультетов кроме факультета
# “Computer Science”.
    ame = session.query(Facultie.Name).filter(Facultie.Name != "Computer Science").all()
    print(ame)