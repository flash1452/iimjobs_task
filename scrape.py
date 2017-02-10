import crawl_comp1 as company1
import crawl_comp2 as company2
import pymysql
conn = pymysql.connect(
    db='company_info',
    user='root',
    passwd='vishal',
    host='localhost')
cursor1 = conn.cursor()
cursor1.execute("SELECT * from company_postings")
result_set = cursor1.fetchall()
for row in result_set:
    company_posting_name = []
    new_posting_details = {}
    cursor2 = conn.cursor()
    cursor2.execute("SELECT detail.posting_id, detail.posting_name, detail.posting_time FROM comp_posting_relation as rel, posting_details as detail where rel.company_id = %d and rel.posting_id = detail.posting_id" % (row[0]))
    posting_det = cursor2.fetchall()
    for result_subset  in posting_det:
        company_posting_name.append(result_subset[1].lower())
    last_updated = posting_det[cursor2.rowcount-1][2]
    if row[1] == "MegasoftInfo":
        company1.comp1_crawling(row[3], company_posting_name, last_updated, new_posting_details)
    else:
        if row[1] == "WeMakeScholars" :
            company2.comp2_crawling(row[3], company_posting_name, last_updated, new_posting_details)
