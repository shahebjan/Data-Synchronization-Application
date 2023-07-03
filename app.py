# <<<---------------------------------------Importing all modules & packages------------------------------------------->>>
import pymysql
# <<<-------------------------------Making database connections--------------------------------->>>
try:
    conn1 = pymysql.connect(host='localhost', user='root', password='', database='data_synchronization_1')
    conn2 = pymysql.connect(host='localhost', user='root', password='', database='data_synchronization_2')
    print("<<<---------------------------------First database------------------------------------>>>")
    with conn1.cursor() as cur:
        sql = '''
        show tables
        '''
        cur.execute(sql)
        conn1.commit()
        data1 = cur.fetchall()
        mytuple1 = data1
        myset1 = set(mytuple1)
        print(myset1)
    print("<<<---------------------------Second database data------------------------------------>>>")
    with conn2.cursor() as cur:
        sql = '''
        show tables
        '''
        cur.execute(sql)
        conn2.commit()
        data2 = cur.fetchall()
        mytuple2 = data2
        myset2 = set(mytuple2)
        print(myset2)
    print("<<<------------------------These tables are available in database1----------------------------->>>")
    x = list(myset1)
    available1 = []
    for i in x:
        for j in i:
            available1.append(j)
    print(available1)
    print("<<<-------------------------These tables are available in database2----------------------------->>>")
    y = list(myset2)
    available2 = []
    for i in y:
        for j in i:
            available2.append(j)
    print(available2)
    print("<<<-------------------------------Coverting into set for comparison------------------------>>>")
    set1 = set(x)
    print(set1)
    set2 = set(y)
    print(set2)
    print("<<<-------------------Fetching the not available table in any database1------------------------------------>>>")
    whole_difference = []
    not_available1 = set2.difference(set1)
    print(not_available1)
    for i in not_available1:
        for k in i:
            whole_difference.append(k)
    print("<<<-------------------Fetching the not available table in any database2------------------------------------>>>")
    not_available2 = set1.difference(set2)
    print(not_available2)
    for i in not_available2:
        for j in i:
            whole_difference.append(j)
    print("<<<----------------------Combining all difference in one list------------------->>>")
    print(whole_difference)
    available1
    available2
    for i in whole_difference:
        if i in available1:
            with conn1.cursor() as cur:
                cur.execute("describe {}".format(i))
                conn1.commit()
                print("<<<------------------This table found in database 1 that i described===>> {}".format(i))
                data1 = cur.fetchall()
                print(data1)
            print("<<<------------------creating a table that is not available in database2====>>> {}".format(i))
            with conn2.cursor() as cur:
                table1 = i
                columns = ""
                for m in data1:
                    columns+=m[0]+" "
                    columns+=m[1]+" "
                    if m[2]=="YES":
                        columns+="NULL, "
                syntax1 = columns[:-2]
                sql=("create table if not exists {} ({})".format(table1, syntax1)+";")
                cur.execute(sql)
                print("Table created===> {}".format(table1))
        elif i in available2:
            with conn2.cursor() as cur:
                cur.execute("describe {}".format(i))
                conn2.commit()
                print("<<<------------------------This table found in database 2 that i described====>> {}".format(i))
                data2 = cur.fetchall()
                print(data2)
            print("<<<---------------------creating this table that is not available in database1====>> {}".format(i))
            with conn1.cursor() as cur:
                table2 = i
                columns = ""
                for m in data2:
                    columns+=m[0]+" "
                    columns+=m[1]+" "
                    if m[2]=="YES":
                        columns+="NULL, "
                syntax2 = columns[:-2]
                sql=("create table if not exists {} ({})".format(table2, syntax2)+";")
                cur.execute(sql)
                print("Table created===> {}".format(table2))
        else:
            print("error")

except Exception as e:
    print(e)                   