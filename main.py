

import cx_Oracle
#Kullanıcı Bilgilerini alamak için
kullaniciAdi = input("İsminiz nedir? ")
sifre= input("Şifreniz nedir? ")
dbAdresi= input("Veri tabanı adresiniz nedir? ")
####################################
conn = cx_Oracle.connect(user=kullaniciAdi, password=sifre, dsn=dbAdresi)
cur = conn.cursor()

tablolari_gosterme = """SELECT owner, table_name FROM all_tables WHERE owner=:kullanici """
cur.execute(tablolari_gosterme,[kullaniciAdi])
liste =cur.fetchall()
dosya= open("log.sql","a")
###################
for varOlanTablo in liste:
 if ((kullaniciAdi, varOlanTablo[1]) and (kullaniciAdi, varOlanTablo[1] + '_LOG') in liste):
  liste.remove(varOlanTablo)
  liste.remove((kullaniciAdi, varOlanTablo[1] + '_LOG'))


print(liste)
#########################
sql = "SELECT * FROM  "
for x in liste:
 cur.execute(sql + x[1])
 data = cur.fetchall()
 col_names = []
 for i in range(0, len(cur.description)):
  col_names.append(cur.description[i][0])

 dosya.write("-----------")
 dosya.write(x[1])
 dosya.write(" tablosu için ------\n")
 dosya.write("create table ")
 dosya.write(x[1])
 dosya.write("_LOG as select * from ")
 dosya.write(x[1])
 dosya.write(" where 1=0")
 dosya.write(";\n/\n")
 dosya.write("alter table ")
 dosya.write(x[1])
 dosya.write("_LOG")
 dosya.write(" ADD( ISLEM_TURU varchar(20), ISLEM_ZAMANI DATE DEFAULT SYSDATE );\n/\n")
 dosya.write("CREATE OR REPLACE TRIGGER ")
 dosya.write(x[1])
 dosya.write("_DELETE_UPDATE_TRG\n AFTER DELETE OR UPDATE OF ")

 #Kolon isimlerini dosyaya yazdırmak için
 z=1
 for y in col_names:
  dosya.write(y)
  if z != len(col_names):
   dosya.write(", ")
  z = z+1
########################################
 dosya.write(" ON ")
 dosya.write(x[1])
 dosya.write("\n")
 dosya.write(" REFERENCING OLD AS OLD NEW AS NEW FOR EACH ROW \n BEGIN \n IF DELETING THEN \n INSERT INTO ")
 dosya.write(x[1])
 dosya.write("_LOG")
 dosya.write("\n(")



 for y in col_names:
  dosya.write(y)
  if z != len(col_names):
   dosya.write(", ")

 dosya.write("ISLEM_TURU")


 dosya.write(")\n VALUES\n (")



 for y in col_names:
  dosya.write(":OLD.")
  dosya.write(y)
  if z != len(col_names):
   dosya.write(", ")
 # z = z+1
 dosya.write("'Silindi'")

 dosya.write(");\nELSIF UPDATING THEN \n INSERT INTO ")
 dosya.write(x[1])
 dosya.write("_LOG")
 dosya.write("\n(")


 for y in col_names:
  dosya.write(y)
  if z != len(col_names):
   dosya.write(", ")

 dosya.write("ISLEM_TURU")

 dosya.write(")\n VALUES\n (")


 for y in col_names:
  dosya.write(":OLD.")
  dosya.write(y)
  if z != len(col_names):
   dosya.write(", ")

 dosya.write("'Güncellendi'")

 dosya.write(");\n END IF;")

 dosya.write("\n END;\n/")

 dosya.write("\n\n")

dosya.close()
















