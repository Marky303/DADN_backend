# Backend đồ án đa ngành

## 1.Introduction
Backend đỉnh cao

## 2.How to install
### 2a.Backend
> [!WARNING]
> Remember to create virtualenv using **virtualenv env** before installing these packages

> [!WARNING]
> Remember to enter virtualenv using **env\Scripts\activate** before installing these packages
```
    pip install -r requirements.txt
```
> [!WARNING]
> Remember to enter backend folder before runserver
```
    python manage.py runserver
```

## 3.Attention
- Customized emails can be modified in backend/account/templates/emails and backend/account/email.py (and settings.py)
- Django data can be deleted using "python manage.py flush"
- Create superuser using "python manage.py createsupauser" (after cd into backend) to create superuser (credentials: nhien/1234)

