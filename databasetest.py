import MySQLdb

class datatest:
    def __init__(self):
        try:
            self.db = MySQLdb.connect(host="localhost", user="cha", passwd="test623",db='testdb')
            self.cursor = self.db.cursor() #make cursor
            self.cursor.execute('''use testdb''') #sql syntax. means 'using testdb'
            self.cursor.execute('''create table if not exists address
                (name char(10), number char(50), etc char(10))''')#create table in testdb
            #make constructor
            print("welcome my testdb!")
            print("we have address database for you")
        except MySQLdb.Error, e:
            print("error : " + str(e))
            
    #입력값을 만드는 함수             
    def insertvalue(self, inputname, inputnumber, inputetc):
        #insert the data in table address using cursor.execute
        self.cursor.execute(u'''insert into `address` values (%s, %s, %s)''',
          (inputname,inputnumber,inputetc))
        self.db.commit() # for store in database.
        print("done!")#for debug
        
    #검색어 찾아주는 함수 
    def searchvalue(self, searchname):
        rs = self.cursor.execute("select*from address where name = %s",(searchname)) 
        #print 출력시 rs값이 숫자로 표현됨. 존재하지 않는다면 0, 존재한다면 1이상의 숫자로 출력.
        #각 상황에 맞게 조건문으로 예외처리 
        if(rs == 0):
            print("unable to find data")
            self.db.rollback()
        else:
            results = self.cursor.fetchall()
            for row in results:
                name = row[0]
                number = row[1]
                etc = row[2]
            print("The data exist!")    
            print("name = " + name , "number = " + number, "etc = " + etc)
    #삭제 함수 (이름만으로 실행할 수 있게 처리)        
    def deletevalue(self, deletename):
        rs = self.cursor.execute("select*from address where name = %s",(deletename))
        if(rs == 0):
            print("Fail beacuse table hava no delete data")
            self.db.rollback()
        else:
            self.cursor.execute("delete from address WHERE name = %s",(deletename))
            print("done")
            self.db.commit()
            
    #메인 실행 함수     
    def mainfunction(self):
        a = True
        while (a) :
            try:
                
                self.select = int(input("please select the number(1.insert 2.search 3.delete 4.quit) :  "))
                if(self.select == 1):
                    print("welcome insert part")

                    username = raw_input("please enter the name :  ")
                    usernumber = raw_input("please enter the nunber :  ")
                    useretc = raw_input("please enter the etc :  ")
                    try:
                        #insertvalue 함수 사용.
                        self.insertvalue(username,usernumber,useretc)
                        restart = raw_input("Do you want quit? than enter the 'y' or, it will restart")
                        if(restart == 'y'):
                            a= False
                        else:
                            continue    
                    # if fail, print error message instead just error and sutdown...
                    except:
                        print("error happen")
                        self.db.rollback()         
             
                #검색 데이터(초기버젼이라 이름만으로 검색가능하게 처리)
                #select*from 문으로 나오는 값을 이용하여 데이터가 존재유무를 가린뒤 각 상황에 맞게 실행하도록 처리               
                elif (self.select == 2):
                    print("search")
                    search = raw_input("enter the what you check name :  ")
                    try:
                        #검색 함수사용 
                        self.searchvalue(search)
                        restart = raw_input("Do you want quit? than enter the 'y' or, it will restart")
                        if(restart == 'y'):
                            a = False
                        else:
                            continue    
                    except:
                        print("error: unable to find such data")
                        self.db.rollback()                   
                #삭제 데이터
                #먼저 삭제할 데이터를 입력받고, 테이블에 존재하는지 검색을 한후 존재한다면 삭제하도록 처리
                elif (self.select == 3):
                    print("delete")
                    deletename = raw_input("enter the delete name :  ")#삭제할 데이터를 입력받음(이름만)
                    try:
                        self.deletevalue(deletename)
                        #종료 또는 진행 문구 
                        restart = raw_input("Do you want quit? than enter the 'y' or, it will restart")
                        if(restart == 'y'):
                            a = False
                        else:
                            continue
                    except MySQLdb.Error, e:
                        print("error : " + str(e))
                        self.db.rollback()                           
                        
                #바로 종료문 
                elif(self.select == 4):
                    print("goodbye")
                    break
            #2개의 except문으로 하나는 mysql 문법상의 문제를 처리하여 알려주고, 하나는 그 이외의 에러가 발생했을시 문구를 띄우고 처음으로 되돌아가게끔 처리
            except MySQLdb.Error, e:
                print("error : " + str(e))    
            except:
                print("you put the worng number please again")
        #커서 종료및 영구 저장, db 종료 
        self.cursor.close()
        self.db.commit()
        self.db.close()
#함수 실행         
a=datatest()
a.mainfunction()
