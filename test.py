import MySQLdb



#make constructor 
try:
    db = MySQLdb.connect(host="localhost", user="cha", passwd="test623",db='testdb')
    cursor = db.cursor() #make cursor
    cursor.execute('''use testdb''') #sql syntax. means 'using testdb'
    cursor.execute('''create table if not exists address
        (name char(10), number char(50), etc char(10))''')#create table in testdb

    #make constructor
    print("welcome my testdb!")
    print("we have address for you")
except MySQLdb.Error, e:
    print("error : " + str(e))

#make select
while True :
    try:
        select = int(input("please select the number(1.insert 2.search 3.delete 4.quit) :  "))
        if(select == 1):
            print("welcome insert part")

            username = raw_input("please enter the name :  ")
            usernumber = raw_input("please enter the nunber :  ")
            useretc = raw_input("please enter the etc :  ")
            
            try:
                #insert the data in table address using cursor.execute
                cursor.execute(u'''insert into `address` values (%s, %s, %s)''',
                          (username,usernumber,useretc))

                db.commit() # for store in database.
                print("done!")#for debug

            #make select for restart or quit
                restart = raw_input("Do you want quit? than enter the 'y' or, it will restart")
                if(restart == 'y'):
                    break
                else:
                    continue
            #make select for restart or quit

            
            # if fail, print error message instead just error and sutdown...
            except:
                print("error happen")
                db.rollback()         
            
            
        #검색 데이터(초기버젼이라 이름만으로 검색가능하게 처리
        #select*from 문으로 나오는 값을 이용하여 데이터가 존재유무를 가린뒤 각 상황에 맞게 실행하도록 처리               
                
        elif (select == 2):
            print("search")
            search = raw_input("enter the what you check name :  ")

            try:
                rs = cursor.execute("select*from address where name = %s",(search)) 
                #print 출력시 rs값이 숫자로 표현됨. 존재하지 않는다면 0, 존재한다면 1이상의 숫자로 출력.
                #각 상황에 맞게 조건문으로 예외처리 
                if(rs == 0):
                    print("unable to find data")
                    continue

                else:                       
                    results = cursor.fetchall()
                    for row in results:
                        name = row[0]
                        number = row[1]
                        etc = row[2]
                        print("The data exist!")    
                        print("name = " + name , "number = " + number, "etc = " + etc)

                    restart = raw_input("Do you want quit? than enter the 'y' or, it will restart")
                    if(restart == 'y'):
                        break
                    else:
                        continue    
                        
            except:
                print("error: unable to find such data")
                db.commit()
                break
            
        #삭제 데이터
        #먼저 삭제할 데이터를 입력받고, 테이블에 존재하는지 검색을 한후 존재한다면 삭제하도록 처리
        elif (select == 3):
            print("delete")
            deletename = raw_input("enter the delete name :  ")#삭제할 데이터를 입력받음(이름만)
            print("searching....")

            rs = cursor.execute("select*from address where name = %s",(deletename))
            if(rs == 0):
                print("Fail beacuse table hava no delete data")
                continue

            else:
                try:
                    cursor.execute("delete from address WHERE name = %s",(deletename))
                    print("done")
                    db.commit()

                    #종료 또는 진행 문구 
                    restart = raw_input("Do you want quit? than enter the 'y' or, it will restart")
                    if(restart == 'y'):
                        break
                    else:
                        continue
                except MySQLdb.Error, e:
                    print("error : " + str(e))
                    db.rollback()
                    break
                    
                
        #바로 종료문 
        elif(select == 4):
            print("goodbye")
            break
        
    
    #2개의 except문으로 하나는 mysql 문법상의 문제를 처리하여 알려주고, 하나는 그 이외의 에러가 발생했을시 문구를 띄우고 처음으로 되돌아가게끔 처리
        
    except MySQLdb.Error, e:
        print("error : " + str(e))    
    
    except:
        print("you put the worng number please again")




cursor.close()
db.commit()
db.close()
