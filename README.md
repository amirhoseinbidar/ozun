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
url : /api/question/
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
    "title": "some title" ,
    "content" : "some content" 
  }
  
  پاسخ :
  {
    "id": 3,
    "answer_set": [], <-- مجموعه آیدی جواب های مرتبط به سوال  در ابتدا خالی است  
    "title": "some text and test", 
    "timestamp": "2019-06-26T17:40:58.354320+04:30", <-- زمان ثبت سوال
    "slug": "some-text-and-test-none", <-- برای استفاده در وبسایت 
    "status": "O" , <-- وضعیت سوال  
    "content": "some content",
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

#### حذف و تغییر سوال 
```
url : /api/question/<id>/
```
متد های قابل قبول :  [ GET, PUT, PATCH, DELETE, ]

#### متد PUT و PATCH
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

 






 
    








    
    
    

