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
url : /rest-auth/login/
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
url : /rest-auth/registration/
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



# درخت درس !!!

اکثرا محتواهای سایت برای ارتباط با یکدیگر از یک گراف درخت استفاده میکنند 
اینکار دسترسی به محتوا های و جستوجو و پیدا کردن نمونه های مرتبط را آسان میکند
نحوه کار آسان است یک درخت از محتوا های موجود در کتاب های درسی موجود است که اشیای مختلف اما با هدف یکسان میتوانند به یکدیگر وصل شوند  و یا در آنها جستوجو کرد به عنوان 
```
/(root): 
  اول :
     ریاضی : ...
     بخوانیم: ...
  دوم : ..
   .
   .
   .
 
   دوازدهم-ریاضی :
      عربی : ... 
      فارسی : ... 
```
بعد دیگر اشیاء میتوانند به یک گره از درخت وصل شوند
```

یک ازمون آمار ---> دوازدهم ریاضی/آمار
دوره آمار و احتمال ---> دوازدهم ریاضی/آمار


مجله زیست ---> دوازدهم تجربی/زیست

```

این کار پیمایش و پیشنهاد را راحت تر میکند مسلما 
شاخه های پایین تر به معنی اختصاصی تر شدن مباحث است

#### نحوه پیمایش در درخت درس موجود در سرویس
```
url : /api/lesson/children/
```

متد های قابل قبول :  [ POST , ]

##### متد POST:

لیستی از زیر شاخه ها را بر میگرداند 

پارامتر های قابل قبول :
  * path : اجباری   , مسیر گره والد , در صورت ارسال / زیر شاخه های اصلی فرستاده میشود
 
مثال :
```
{
  "path" : "/"
}

result:
[
    {
        "id": 1,
        "content": "دهم",
        "depth": 1,
        "numchild": 2
    },
    {
        "id": 3,
        "content": "یازدهم-ریاضی",
        "depth": 1, <-- عمق گره
        "numchild": 1 <-- (در صورت 0 بودن تعداد فرزند دیگر ریکویست نزنید برای کم شدن ترافیک سرویس)
    },
    ...
    ...
    ...
]

or

{
  "path" : "دهم" ,
}

result:
[
    {
        "id": 2,
        "content": "ریاضی",
        "depth": 2,
        "numchild": 0
    },
    {
        "id": 7,
        "content": "فیزیک",
        "depth": 2,
        "numchild": 0
    }
]

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
  * tags : تگهای مرتبط به سوال

مثال:
```
  {
    "title": "Repair Phone" ,
    "content" : "I break my brother phone how can I repair it?" ,
    "tags" : [ "phone" , "mistake" , "breake" ]
  }
  
  پاسخ :
  {
    "id": 3,
    "answer_set": [], <-- مجموعه آیدی جواب های مرتبط به سوال  در ابتدا خالی است  
    "tags" :  [
      "phone",
      "mistake",
      "break"
    ]
    "title": "Repair Phone", 
    "timestamp": "2019-06-26T17:40:58.354320+04:30", <-- زمان ثبت سوال
    "slug": "Repair-Phone", <-- برای استفاده در وبسایت 
    "status": "O" , <-- وضعیت سوال  
    "content": "I break my brother phone how can I repair it?",
    "has_answer": false,
    "total_votes": 0, <-- امتیاز سوال -به این صورت محاسبه میشود
                            total_vote = UpVotes - DownVotes
    
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
    "content" : "WHAT the fuck did you do with my phone?!! , I WILL KILL YOOOOOOU",
    "question" : 3
  }
  
  response: 
  {
    "id": 1,
    "content": "WHAT the fuck did you do with my phone?!! , I WILL KILL YOOOOOOU",
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

در صورت صحیح بودن آیدی ارسالی دیگر جوابی  که انتخاب شده اگر جوابی قبلا انتخاب شده باشد  
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

### جستوجو در سوالات

```
url : /api/qa/question/search/
```

متد های قابل قبول :  [ POST, ]

پارامتر های قابل قبول :
  * text 
  * tag

نکته: حداقل یکی از پارامتر ها باید فرستاده شود
متن ارسالی در عنوان و متن جستوجو میشود

مثال:
```
{
  "text" : "ozun"
  "tag" : ["website" , "education" , "app"]
}

result :
{
  < question 1> ,
  < question2 > , 
  ...
}
```



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
  * lesson : درس مرتبط با مجله - اختیاری
  
مثال :
```
{
  "title": "about a eminem",
  "content" : "a raper who say everyone is asshole and he is better than 2pac :/" ,
  "lesson" : "rapers/personality"
}

respons:
{
    "id": 1,
    "slug": "about-a-eminem",
    "title": "about a eminem",
    "content": "a raper who say everyone is asshole and he is better than 2pac :/",
    "timestamp": "2019-06-26T21:29:36.111120+04:30",
    "user": 8,
    "lesson" : "rapers/personality"
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
  * lesson : درس مرتبط با مجله - اختیاری
  
  
مثال :
```
{
  "title": "about eminem",
  "content" : "a raper who say everyone is asshole and he is better than 2pac :/
               (sorry ,who say everyone is motherfu*** asshole) " ,
  "lesson" : "rapers/personality"  
}

respons:
{
    "id": 1,
    "slug": "about-eminem",
    "title": "about eminem",
    "content": "a raper who say everyone is asshole and he is better than 2pac :/
               (sorry ,who say everyone is motherfu*** asshole) ",
    "timestamp": "2019-06-26T21:29:36.111120+04:30",
    "user": 8,
    "lesson": "rapers/personality"  
}
```

### جستوجو در مجله ها
```
url: /api/magazine/search/
```

پارامتر های قابل قبول :
  * text 
  * path : درس مرتبط با مجله
  
مثال :
```
{
  "text": "eminem",
  "path": "rapers/personality" 
}

result:
{
  <magazine about eminem>,
  <magazine about eminem>,
  ...
}
```

### بازخورد به مجله 
```
url: /api/magazine/feedback/<id>/
```
پارامتر های مورد نیاز :
  * feedback_type : [ "U"(UpVote)  or "D"(DownVote) or "F"(Favorite) ]
  مقدار فیویریت برابر با امتیاز مثبت  است و نشانه گذاری مجله برای دسترسی بعدی 
  استفاده میشود - این قابلیت تحت توسعه است آن را نادیده بگیرید
  
مثال:
```
{
  "feedback_type" : "U" ,
}

result:
"feedback recorded"

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
  * lesson : درس مرتبط با با کورس - اختیاری
  
مثال :
```
{
  "title": "about cryptography",
  "content" : "I dont know what is it but seems good :D",
  "lesson" : "math/cryptography/view" 
}

respons:
{
    "id": 1,
    "slug": "about-cryptography",
    "title": "about cryptography",
    "content": "I dont know what is it but seems good :D",
    "timestamp": "2019-06-26T21:29:36.111120+04:30",
    "user": 8,
   "lesson" : "math/cryptography/view"
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
  * lesson : درس مرتبط با با کورس - اختیاری
  
مثال :
```
{
  "title": "about cryptography",
  "content" : "I dont know what is it but seems good :D ... after 3 month:  noooo hellllllll 
  cryptography is a fu*** hard my mind shit when I want solve its questions :( ",
  "lesson" : "math/cryptography/view" 
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
    "lesson" : "math/cryptography/view"
}
```
 
 ### جستوجو در مجله ها
```
url: /api/magazine/search/
```

پارامتر های قابل قبول :
  * text 
  * path : درس مرتبط با مجله
  
مثال :
```
{
  "path": "math/cryptography" 
}

result:
{
  <course about cryptography>,
  <course about cryptography>,
  ...
}
```

### بازخورد به مجله 
```
url: /api/course/feedback/<id>/
```
پارامتر های مورد نیاز :
  * feedback_type : [ "U"(UpVote)  or "D"(DownVote) or "F"(Favorite) ]
  مقدار فیویریت برابر با امتیاز مثبت  است و نشانه گذاری مجله برای دسترسی بعدی 
  استفاده میشود - این قابلیت تحت توسعه است آن را نادیده بگیرید
  
مثال:
```
{
  "feedback_type" : "D" ,
}

result:
"feedback recorded"

```

## Quiz

کوییز ها برای آزمون ها استفاده میشوند این بخش باعث میشود که 
کاربران بتوانند در ساختن کوییز ها کمک کنند و در عوض آن نیز امتیاز بگیرند
البته این امکان هم هست که کاربران کوییز هایی که میخواهند انتخاب کنند
و یک پی دی اف برای برگه آزمون و یک پی دی اف دیگر برای برگه پاسخ آزمون به
آنها تحویل داده شود  


#### ساختن و لیست کردن تمام کوییزها بر اساس زمان ایجاد شدن
```
url: /api/course/feedback/<id>/
```

متد های قابل قبول :  [ GET, POST ]

##### POST

پارامتر های مورد نیاز :
  * content :   اجباری , قابلیت ارسال مدیا
  * answer_set :  لیستی از مجموعه جواب ها , اجباری 
    * content :  اجباری 
    * is_correct_answer : اجباری 
  * exponential_answer : پاسخ تشریحی کوییز , اختیاری , قابلیت ارسال مدیا 
  * lesson : مسیر مرتبت به کوییز , اجباری
  * source :  منبعی که کوییز از آن طرح شده ,  اجباری
  * level : سطح سوال , اجباری
  * time_for_out :  زمان مورد نیاز بزای پاسخ گویی در صورت خالی بودن بر اساس لول تنظیم میشود ,اختیاری 

مثال:
```
{
	"content" : "how much average time take  for a girl to dress and ready for going out ? " ,
	"answer_set" : [
			{ "content" : "1 hour" , "is_correct_answer" : false } ,
			{ "content" : "3 hour" , "is_correct_answer" : false } ,
			{ "content" : "more than 1 day" , "is_correct_answer" : true } ,
			{ "content" : "infinite " , "is_correct_answer" : false }
	],
	"exponential_answer" : " well of course it depend on girl but between 1 day and 1 week is good \n for whom tick first      answer I should say joke with yourself pls :| , and for tick fourth answer be careful we said average !!! ",
	"lesson" : "girls/behavior/understanding" ,
	"source" : "strange girls !" ,
	"level" : "VH" <-- choices are VE:very easy , E:easy , M:medium , H:hard , VH:very hard
	"time_for_out" : "01:00:00"
}

result:

{
    "id": 6,
    "content": "how much average time take  for a girl to dress and ready for going out ?",
    "answer_set": [
        {
            "id": 21,
            "content": "1 hour",
            "is_correct_answer": false
        },
        {
            "id": 22,
            "content": "3 hour",
            "is_correct_answer": false
        },
        {
            "id": 23,
            "content": "more than 1 day",
            "is_correct_answer": true
        },
        {
            "id": 24,
            "content": "infinite",
            "is_correct_answer": false
        }
    ],
    "exponential_answer" : " well of course it depend on girl but between 1 day and 1 week is good \n for whom tick first       answer I should say joke with yourself pls :| , and for tick fourth answer be careful we said average !!! ",
	  "lesson" : "girls/behavior/understanding" ,
	  "source" : "strange girls !" ,
    "level": "VH",
    "time_for_out": "01:00:00",
    "user": 3, <-- user that write this question
    "total_votes": 0 
}
```
  
##### GET

مثال :
```
  {
    "count": all quizzes count,
    "next": url to get next ten quiz,
    "previous": url to get previous ten quiz,
    "results": [
      < quiz 1> ,
      < quiz 2> , 
      .
      .
      .
    ]
```

#### ادیت , حذف و گرفتن اطلاعات یک کوییز

متد های قابل قبول :  [ GET, PUT ,PATCH , DELETE ]

```
	url : /api/quiz/<id>/
```

##### DELETE 
respnse 204 

##### PUT , PATCH

مثال:
```
{
	"content" : "how much average time take  for a girl to dress and ready for going out ? " ,
	"answer_set" : [
			{ "content" : "1 hour" , "is_correct_answer" : false } ,
			{ "content" : "3 hour" , "is_correct_answer" : false } ,
			{ "content" : "more than 1 day" , "is_correct_answer" : true } ,
			{ "content" : "infinite " , "is_correct_answer" : false }
	],
	"exponential_answer" : " well of course it depend on girl but between 1 day and 1 week is good \n for whom tick first answer I should say joke with yourself pls :| , for third answer it is close but there is handful girls who can do it and for tick fourth answer be careful we said average !!! ",
	"lesson" : "girls/behavior/understanding" ,
	"source" : "strange girls !" ,
	"level" : "VH" <-- choices are VE:very easy , E:easy , M:medium , H:hard , VH:very hard
	"time_for_out" : "01:00:00"
}

result:

{
    "id": 6,
    "content": "how much average time take  for a girl to dress and ready for going out ?",
    "answer_set": [
        {
            "id": 21,
            "content": "1 hour",
            "is_correct_answer": false
        },
        {
            "id": 22,
            "content": "3 hour",
            "is_correct_answer": false
        },
        {
            "id": 23,
            "content": "more than 1 day",
            "is_correct_answer": true
        },
        {
            "id": 24,
            "content": "infinite",
            "is_correct_answer": false
        }
    ],
    "exponential_answer" : "  well of course it depend on girl but between 1 day and 1 week is good \n for whom tick first answer I should say joke with yourself pls :| , for third answer it is close but there is handful girls who can do it and for tick fourth answer be careful we said average !!!" ,
	  "source" : "strange girls !" ,
    "level": "VH",
    "time_for_out": "01:00:00",
    "user": 3, <-- user that write this question
    "total_votes": 0 
}
```


##### GET 
```
	{ < quiz> }
```

#### جستوجو در کوییز ها
```
url : /api/quiz/search/
```


متد های قابل قبول :  [  POST, ]
 

پارامتر های مورد نیاز : 
  * حداقل یکی از پارامتر های زیر باید فرستاده شود
  * text : کلمات موجود در عنوان و محتوا جستوجو میشوند 
  * path : مسیر سوال

مثال :
```
{
	"text" : "tricks for attract a girl" , 
	"path" : "girl/attention" , 
}

result : 
{
	<quiz 1> ,
	<quiz 2> , 
	.
	.
	.
}
```


#### گرفتن  تمام کوییز ها به ترتیب بیشترین امتیاز
```
	url: /api/quiz/most-vote/
```

متد های قابل قبول :  [  GET, ]
 

#### بازخورد به یک کوییز
```
	url: /api/quiz/feed-back/<id>/
```

متد های قابل قبول :  [  POST, ]
 

پارامتر های مورد نیاز :
   *  feedback_type : U or D --- U:UP_VOTE , D:DOWNVOTE  
	
مثال 
```
{ "feedback_type" : "U" }

result:
"feedback recorded"

```

## EXAM 
 در واقع سیستم آزمون از کوییز ها استفاده میکند و یک ازمون میسازد و آن را مدیریت میکند 
 تا زمان آزمون به پابان برسد در نهایت پاسخ ها و سوال ها را آنالیز کرده و نتایح آنالیز و 
 نمونه اکزم اصلی را ارشیو میکند


#### شروع یک آزمون
```
url : /api/exam/start/
```

متد های قابل قبول :  [  POST, ]

پارامتر های مورد نیاز :
  path :  مسیری که میخواهیم از آنجا کوییز ها را برداریم و بک آزمون تشکیل دهیم , اجباری
  number : تعداد کوییزها , پیشفرض ۷ کوییز , اختیاری
  source :  منبعی که کوییزها باید از آنجا برداشته شوند , اختیاری
  level : مقدار سختیه کوییزها , اختیاری
  
نکته : 
   در صورت که به اندازه تعداد مورد نظری که در پارامتر فرستاده میشود کوییز در سرویس وجود نداشت
   باشد  با تمام کوییز های موجود یک آزمون ایجاد میشود
   
   بعد از اتمام زمان امتحان سوال بسته و آرشیو میشود
   
مثال :
```
{
	"path" : "girl/attention" ,
	"number" : 10 ,
	"source" : "strange girls !" ,
	"level" : "VH" <-- "choices are VE:very easy , E:easy , M:medium , H:hard , VH:very hard"
}

result:
[
    {
        "id": 28, 
        "close_date": "2019-07-19T15:33:11.722991+04:30", <-- time that exam stated 
        "add_date": "2019-07-19T14:11:41.748627+04:30", <-- time that exam will end (note: you can calculate exam time with  close_date - add_date )
        "time_zone": "Asia/Tehran",  <-- time_zone to don't confuse add and close date for diffrent location
        "quizstatus_set": [ <-- collection of quizzes exists in exam and thair status 
            {
                "status_id": 55,
                "quiz": { <-- real quiz
                    "content": "how much average time take  for a girl to dress and ready for going out ?",
                    "answer_set": [
                        {
                            "id": 21,
                            "content": "1 hour"
                        },
                        {
                            "id": 22,
                            "content": "3 hour"
                        },
                        {
                            "id": 23,
                            "content": "more than 1 day"
                        },
                        {
                            "id": 24,
                            "content": "infinite"
                        }
                    ],
                    "lesson": "girl/attention",
                    "source": "strange girls !",
                    "level": "VH",
                    "time_for_out": "01:00:00", <-- average time a student can answer this quiz
                    "user": 3
                },
                "did_user_answer": false, <-- read_only attrebute
                "user_answer": null <-- answer id that user selected it is null at first you should full it with update exam
            },
	    { <quiz_status 2>} ,
	    { <quiz_status 3>} ,
	    	.
	    	.
	    	.
	    { <quiz_status 10>}
	]
    }
]
	 
```

#### آپدیت یک آزمون
```
url : /api/exam/update/
```
نکته :
   بعد از پایان زمان یک امتحان قادر به پاسخ گویی نیسنید
   ازمون اکتیو اپدیت خواهد شد
   
متد های قابل قبول :  [  PUT,PATCH, ]

پارامتر های مورد نیاز :
    id : ایدی وضعیت سوال  
    user_answer : ایدی جوابی که کاربر انتحاب کرده است

مثال :
```
{
    "quizstatus_set" : [
    	{ "status_id": 55 , "user_answer": 24 } ,
	{ "status_id": <another stauts id> , "user_answer": <a id that is in quiz answers >},
		.
		.
		.
    ]
}

result: 
{
    "id": 28,
    "close_date": "2019-07-19T15:33:11.722991+04:30",
    "add_date": "2019-07-19T14:11:41.748627+04:30",
    "time_zone": "Asia/Tehran",
    "quizstatus_set": [
        {
            "status_id": 55,
            "did_user_answer": true,
            "quiz": 6,
            "user_answer": 24
        },
        {
            "status_id": 56,
            "did_user_answer": false,
            "quiz": 5,
            "user_answer": null
        }
	.
	.
	.
    ]
}

```

#### بستن یک آزمون
```
url : /api/exam/finish/
```
   
متد های قابل قبول :  [ GET, ]


مثال :
```
get --> url

result :

{
  'notification' : 'exam finished successfully',
  'exam_pk' : 28,
  'add_date' : "2019-07-19T14:11:41.748627+04:30",
  'close_date' : "2019-07-19T15:33:11.722991+04:30", 
}
```

#### نمایش اطلاعات ازمون 

```
url : /api/exam/info/<id>/
```

در صورتی که به جای ایدی کلمه  
active  
را بنویسید ازمون فعال برای شما ارسال میشود

جواب سوال ها فقط بعد از اتمام ازمون قابل دسترسی است


متد های قابل قبول :  [ GET, ]


مثال :
```
get --> /api/exam/info/28/

{
    "id": 28,
    "close_date": "2019-07-19T15:33:11+04:30",
    "add_date": "2019-07-19T14:11:41.748627+04:30",
    "time_zone": "Asia/Tehran",
    "quizstatus_set": [
        {
            "status_id": 55,
            "quiz": {
                "id": 6,
                "content": "how much average time take  for a girl to dress and ready for going out ?",
                "answer_set": [
                    {
                        "id": 21,
                        "content": "1 hour",
                        "is_correct_answer": false <--- after closing exam this will appear
                    },
                    {
                        "id": 22,
                        "content": "3 hour",
                        "is_correct_answer": false
                    },
                    {
                        "id": 23,
                        "content": "more than 1 day",
                        "is_correct_answer": true
                    },
                    {
                        "id": 24,
                        "content": "infinite",
                        "is_correct_answer": true
                    }
                ],
                "exponential_answer": "",
                "lesson": "دهم/ریاضی",
                "source": "نشر الگو",
                "level": "VH",
                "time_for_out": "01:00:00",
                "user": 3,
                "total_votes": 1
            },
            "did_user_answer": true,
            "user_answer": 24
        },
	.
	.
	.
     ]
}
```

