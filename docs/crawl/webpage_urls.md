برای پیدا کردن آدرس صفحه بازیکنا باید اول صفحه لیگ ها رو بگیریم و از داخلش آدرس صفحه تیم ها رو پیدا کنیم و از داخل صفحه تیم ها آدرس صفحه بازیکنا رو پیدا کنیم

آدرس صفحه لیگ ها به این فرمته:

https://www.transfermarkt.com/{league_name}/startseite/startseite/wettbewerb/{Country_abbreviation}/plus/?saison_id={year}

e.g. https://www.transfermarkt.com/premier-league/startseite/wettbewerb/GB1/plus/?saison_id=2022

سه تا متغیر داره که اسم لیگ و مخفف کشور رو دستی میتونیم پیدا کنیم و سال رو هم میتونیم از 2015 تا 2021، iterate کنیم.وقتی به این آدرس ها ریکوئست میزنیم دو تا جدول از تیم هایی که تو فصل مورد نظر توی لیگ مورد نظر بودن بهمون نشون میده.

هر کدوم از لینک های تیم ها رو که باز کنیم یکی از دو تا فرمت پایین رو داره:

1- https://www.transfermarkt.com/{team_name}/startseite/verein/{team_id}/saison_id/{year}

e.g. https://www.transfermarkt.com/manchester-city/startseite/verein/281/saison_id/2021

2- https://www.transfermarkt.com/{team_name}/spielplan/verein/{team_id}/saison_id/{year}

e.g. https://www.transfermarkt.com/manchester-city/spielplan/verein/281/saison_id/2021

اینجا هم سه تا متغیر داریم. اسم تیم و آیدی تیم رو نمیشه به راحتی جنریت کرد و لازمه از جدول لیگ پیدا کنیم ولی سال رو میشه با iteration در آورد
فرق دو تا فرمتی که برای آدرس تیم ها هست هم اینه که وقتی فرمت اول رو باز میکنیم به لیست بازیکنا دسترسی داریم و وقتی فرمت دوم رو باز میکنیم به لیست بازی های تیم توی هر لیگ توی فصل مربوط دسترسی داریم

توی فرمت اول لینک هر بازیکنی رو باز کنیم به این شکله:

https://www.transfermarkt.com/{player_name}/profil/spieler/{player_id}

e.g. https://www.transfermarkt.com/ederson/profil/spieler/238223

داخل صفحه بازیکنا که با این url باز میشه اطلاعات زیر موجوده:

1- date of birth

2- citizenship

3- height

4- foot
