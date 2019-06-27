# OZUN REST API 0.1.0

آدرس ای پی آی تست ازون: 
 * https://amirhoseinbidar.pythonanywhere.com
یوزر تست : 
 * username = root
 * password = h2oso2co2
 * email = root@toor.com
  
نکته: 
برخی از متد ها دارای قابلیت 
دریافت مدیا هستند به این صورت که قابلیت ذخیره متن و عکس 
به صورت همزمان در آنها وجود دارد   
نکته مهم :  
این اطلاعات فقط از طریق   
form-data/multipart  
میتوانند فرستاده شوند قالب جیسون قابلیت ارسال اطلاعات باینری را ندارد  
  
  
مثال : 
```
نحوه فرستان  اطلاعات
{
  "content" : "
    this is a test text and I have a Image {%% 0 %%} and another {{%% 1 %%}}
    and this is repeat {%% 0 %%}
  ",
  "content2" : "
    and a good image {%% 1 %%}
  "
  "media" : [<image_a.jpg>,<image_b.png>]
}

پس از ارسال به این طورت ذخیره میشود 
{
  "content": "
    this is a test text and I have a Image www.domain.com/media/media/image_a.jpg and another www.domain.com/media/media/image_b.png
    and this is repeat www.domain.com/media/media/image_a.jpg
  "
  "content" : "
    and a good image  www.domain.com/media/media/image_b.png
  "
}



```

## ورود به ازون 
شما میتوانید از طریق لاگین یا ثبت نام وارد شوید 



### ورود از طریق لاگین
```
url : /api/rest-auth/login/
```
متد های قابل قبول :  [ POST, ]

پارامتر های قابل قبول :
  * username :  اختیاری برابر نام کاریری کابر است
  * email : اختیاری برابر با ایمیل کاربر است
  * password : الزامی برابر با پسورد کاربر است

نکته یوزرنیم و ایمیل اختیاری هستند ولی برای ورود یوزنیم یا ایمیل باید فرستاده شود

مثال :
```
  {
    "username": "root",
    "password": "h2oso2co2"
  }
  
  or
  
  {
    "email": "root@toor.com",
    "password" : "h2oso2co2"
  }
  
  
  پاسخ: 
  {
    "token" : "<A RANDOM TOKEN>"
  }
  
```

### ورود از طریق ثبت نام
نکته: ایمیل تایید هنوز فرستاده نمیشود
```
url : /api/rest-auth/registration/
```

متد های قابل قبول :  [ POST, ]

پارامتر های قابل قبول :
   * username : الزامی نام کاربر 
   * email: اختیاری برای اطلاع رسانی و بازیابی رمز عبور کابر 
   * password1: رمز عبور کاربر
   * password2: تکرار رمز عبور صرفا جهت چک کردن

مثال :
```
  {
    "username": "amirhosein_bidar",
    "email" : "amirhoseinbk00@gmai.com",
    "password1": "some_pass",
    "password2": "some_pass"
  }
  
  پاسخ: 
  {
    "token" : "<A RANDOM TOKEN>"
  }
  
```

## سیستم پرسش و پاسخ

#### ایجاد یک پرسش و گرفتن سوالات بر اساس آخرین  سوال پرسیده شده
```
url : /api/qa/question/
```
متد های قابل قبول :  [ POST , GET, ]

##### متد POST:
 
برای ساختن یک پرسش میتوانید از این متد استفاده کنید استفاده کنید

پارامتر های قابل قبول :
  * title : عنوان سوال 
  * content : محتوای سوال دارای قابلیت دریافت مدیا 
  
مثال:
```
  {
    "title": "Repair Phone" ,
    "content" : "I break my brother phone how can I repair it?" 
  }
  
  پاسخ :
  {
    "id": 3,
    "answer_set": [], <-- مجموعه آیدی جواب های مرتبط به سوال  در ابتدا خالی است  
    "title": "Repair Phone", 
    "timestamp": "2019-06-26T17:40:58.354320+04:30", <-- زمان ثبت سوال
    "slug": "Repair-Phone", <-- برای استفاده در وبسایت 
    "status": "O" , <-- وضعیت سوال  
    "content": "I break my brother phone how can I repair it?",
    "has_answer": false,
    "total_votes": 0, 
    "user": 8 <-- آیدی کاریری که سوال را پرسیده است
  }
  NOTE : O mean question is OPEN and C mean question is Closed 
```

##### متد GET:
تمام سوال ها را بر اساس زمان بازمیگرداند
مثال :
``` 
 GET --> url 
 
 پاسخ
 [
    {  Question1 },
    {  Question2 },
    ...
 ]
```

####   حذف و تغییر سوال و نمایش یک سوال بر اساس آیدی 
```
url : /api/qa/question/<id>/
```
متد های قابل قبول :  [ GET, PUT, PATCH, DELETE, ]

##### متد PUT و PATCH :
 تغییر محتوا و  وضعیت 
 
 مثال :
 ```
  PUT or PATCH -->  /api/question/3/
  with :
    {
      "status" : "C"
    }
  
  response :
    {
      "id" : 3 , 
      ...
      status : "C",
      ...
    }
 ```
 
#### ایجاد جواب 
 ```
 url : /api/qa/answer/
 ```
 
پارامتر های قابل قبول :
  * title : عنوان پاسخ 
  * content : محتوای پاسخ دارای قابلیت دریافت مدیا 
  * question :  آیدی سوال مخاطب
  
متد های قابل قبول :  [ POST, ]

مثال :
```

  {
    "content" : "WHAT the fuck did you do with my phone , I WILL KILL YOOOOOOU",
    "question" : 3
  }
  
  response: 
  {
    "id": 1,
    "content": "WHAT the fuck did you do with my phone , I WILL KILL YOOOOOOU",
    "total_votes": 0,
    "timestamp": "2019-06-26T19:53:11.316598+04:30",
    "is_answer": false, <-- این فیلد از طرف فرستنده سوال تایید میشود
    "question": 3,
    "user": 13 
  }

```


####   حذف و تغییر سوال و نمایش یک سوال بر اساس آیدی 
```
url : /api/qa/answer/<id>/
```
متد های قابل قبول :  [ GET, PUT, PATCH, DELETE, ]


#### تایید جواب 

```
url : /api/qa/accept-answer/
```

در صورت صحیح بودن آیدی ارسالی دیگر جوابی  که انتخاب شده (اگر جوابی قبلا انتخاب شده باشد )  ـ 
is_answer = false  
میشود و جواب درخواستی  
is_answer = true   
میشود

متد های قابل قبول :  [ POST, ]

پارامتر های قابل قبول :
  * answer: آیدی پاسخی که میخواهیم تایید شود

مثال :
```
  {
    "answer" : 1  
  }
  
  response :
  {
    "status": true
  }
```

#### امتیاز دادن به سوال


```
url : /api/qa/question/vote/
```

متد های قابل قبول :  [ POST, ]

پارامتر های قابل قبول :
  * question: آیدی سوالی که میخواهیم امتیاز دهیم
  * feedback_type: نوع بازخورد Upvote or Downvote

مثال :
```
{
  "question" : 3
  "feedback_type" : "U"  <-- or "D" ("U" for Upvote and "D" for Downvote )
}
```

#### امتیاز دادن به جواب

```
url : /api/qa/answer/vote/
```

متد های قابل قبول :  [ POST, ]

پارامتر های قابل قبول :
  * answer: آیدی سوالی که میخواهیم امتیاز دهیم
  * feedback_type: نوع بازخورد Upvote or Downvote

مثال :
```
{
  "answer" : 1
  "feedback_type" : "U"  <-- or "D" ("U" for Upvote and "D" for Downvote )
}
```

#### ارسال سوال های پاسخ داده شده

```
url : /api/qa/question/answered/
```

متد های قابل قبول :  [ Get, ]

#### ارسال سوال های پاسخ داده نشده

```
url : /api/qa/question/unanswered/
```
متد های قابل قبول :  [ Get, ]


## Magazine و  Course :

#### ساختن و لیست کردن تمام مجله ها بر اساس زمان ایجاد شدن
```
url : /api/magazine/
```

متد های قابل قبول :  [ Get, Post, ]

##### POST:
 
پارامتر های قابل قبول :
  * title 
  * content : دارای قابلیت گرفتن مدیا

مثال :
```
{
  "title": "about a eminem"
  "content" : "a raper who say everyone is asshole and he is better then 2pac :/"
}

respons:
{
    "id": 1,
    "slug": "about-a-eminem",
    "title": "about a eminem",
    "content": "a rapper who say everyone is asshole and he is better then 2pac :/",
    "timestamp": "2019-06-26T21:29:36.111120+04:30",
    "user": 8,
    "lesson": null <-- Under develop ignore it
}
```

####  اصلاح و حذف و نمایش یک مجله

```
url : /api/magazine/<id>/
```

متد های قابل قبول :  [ GET, PUT, PATCH, DELETE, ]


##### PUT and PATCH:
 
پارامتر های قابل قبول :
  * title 
  * content : دارای قابلیت گرفتن مدیا

مثال :
```
{
  "title": "about eminem"
  "content" : "a raper who say everyone is asshole and he is better then 2pac :/
               (sorry ,who say everyone is motherfu*** asshole) "
}

respons:
{
    "id": 1,
    "slug": "about-eminem",
    "title": "about eminem",
    "content": "a raper who say everyone is asshole and he is better then 2pac :/
               (sorry ,who say everyone is motherfu*** asshole) ",
    "timestamp": "2019-06-26T21:29:36.111120+04:30",
    "user": 8,
    "lesson": null <-- Under develop ignore it
}
```


#### ساختن و لیست کردن تمام کرس ها بر اساس زمان ایجاد شدن
```
url : /api/course/
```

متد های قابل قبول :  [ Get, Post, ]

##### POST:
 
پارامتر های قابل قبول :
  * title 
  * content : دارای قابلیت گرفتن مدیا

مثال :
```
{
  "title": "about cryptography"
  "content" : "I dont know what is it but seems good :D"
}

respons:
{
    "id": 1,
    "slug": "about-cryptography",
    "title": "about cryptography",
    "content": "I dont know what is it but seems good :D",
    "timestamp": "2019-06-26T21:29:36.111120+04:30",
    "user": 8,
    "lesson": null <-- Under develop ignore it
}
```

####  اصلاح و حذف و نمایش یک کرس

```
url : /api/course/<id>/
```

متد های قابل قبول :  [ GET, PUT, PATCH, DELETE, ]


##### PUT and PATCH:
 
پارامتر های قابل قبول :
  * title 
  * content : دارای قابلیت گرفتن مدیا

مثال :
```
{
  "title": "about cryptography"
  "content" : "I dont know what is it but seems good :D ... after 3 month:  noooo hellllllll 
  cryptography is a fu*** hard my mind shit when I want solve its questions :( "
}

respons:
{
    "id": 1,
    "slug": "about-cryptography",
    "title": "about cryptography",
    "content": "I dont know what is it but seems good :D ... after 3 month:  noooo hellllllll 
  cryptography is a fu*** hard my mind shit when I want solve its questions :( ",
    "timestamp": "2019-06-26T21:29:36.111120+04:30",
    "user": 8,
    "lesson": null <-- Under develop ignore it
}
```
 
  

  