# All Required Libraries
from bs4 import BeautifulSoup
import favicon as fi
import feedparser as fp
from mechanize import Browser
import pandas as pd
import sqlite3 as sql
import requests
import re
import datetime
import ssl
# import smtplib
# from email.mime.multipart import MIMEMultipart
# from email.mime.text import MIMEText

# Connect To DataBase
connect = sql.connect('db.sqlite3')
conn = connect.cursor()

# SSL Connection
ssl._create_default_https_context = ssl._create_unverified_context

# Adding Data into The Created Table's in DataBase
def add_Name_Icon(name, icon):
    try:
        conn.execute('INSERT INTO endpoints_rss_feed_name_icon(feedName, feedIcon, feedFrequency_accepted, feedFrequency_reject) VALUES (?,?,?,?)',(name, icon, 0, 0))
    except:
        pass
    connect.commit()


def add_database(name, Title, Published_Date, Link, Summary):
    try:
        conn.execute('INSERT INTO endpoints_rss_feed_database(feedName, title, publishedDate, link, summary) VALUES (?,?,?,?,?)',(name, Title, Published_Date, Link, Summary))
    except:
        pass
    connect.commit()

# def add_database(name, Title, Published_Date, Link, Summary):
#     try:
#         # Check Article is present in endpoints_rss_feed_database table or not
#         conn.execute('SELECT id FROM endpoints_rss_feed_database WHERE title = ?',(Title,))
#         result = conn.fetchone()
#         if result is None:
#             # Check Article is present in endpoints_rss_feed_temp table or not
#             conn.execute('SELECT id FROM endpoints_rss_feed_temp WHERE title = ?',(Title,))
#             check = conn.fetchone()
#             conn.execute('INSERT INTO endpoints_rss_feed_temp(feedName, title, publishedDate, link, summary) VALUES (?,?,?,?,?)',(name, Title, Published_Date, Link, Summary))
#             if check is None:
#                # Send Mail to Admin For New Article Is Insert into Database
#                msg = MIMEMultipart()
#                msg.set_unixfrom('author')
#                msg['From'] = 'cyberbriefs.onesmarter@gmail.com'
#                msg['To'] = 'vikram@vikramsethi.com'
#                msg['Subject'] = 'CyberBriefs DataBase_Feed: {}'.format(name)
#                html = f"""
#                 <html>
#                 <body>
#                 <h3>Title: {Title}</h3>
#                 <h4>Published Date: {Published_Date}</h4>
#                 <h4>Summary: {Summary}</h4>
#                 <a type="button" href="https://backend.cyberbriefs.internsprogram.com/api/accept/{Title}" style="text-decoration:none; border-radius: 10px; border:none; color:white; padding:10px 20px; background: limegreen;">Accept</a>
#                 <a type="button" href="https://backend.cyberbriefs.internsprogram.com/api/reject/reject" style="text-decoration:none; border-radius: 10px; border:none; color:white; padding:10px 20px; background: tomato;">Reject</a>
#                 </body>
#                 </html>    
#                """
#                msg.attach(MIMEText(html, 'html'))
#                mailserver = smtplib.SMTP_SSL('smtpout.secureserver.net', 465)
#                mailserver.ehlo()
#                mailserver.login('cyberbriefs.onesmarter@gmail.com', 'xmcjrzeovgbktjed')
#                response = mailserver.sendmail('cyberbriefs.onesmarter@gmail.com','vikram@vikramsethi.com',msg.as_string())
#                print('Mail is Send!!')
#                mailserver.quit()
#                # Ending for Send Mail To Admin
#     except:
#         pass
#     connect.commit()
# Ending For Adding Data in DataBase Table's

   
# Fetching All RSS_Feed_URL in DataBase Table
conn.execute("SELECT feedUrl FROM endpoints_rss_feed_url")
RSS_Feed_URL = conn.fetchall()
urls = [i[0] for i in RSS_Feed_URL]
# Ending of Fetching RSS_Feed_URL in DataBase Table


# Fetching All KeyWords in DataBase Table
conn.execute("SELECT keywords FROM endpoints_rss_feed_keyowrds")
RSS_Feed_KeyWords = conn.fetchall()
search_word = [i[0] for i in RSS_Feed_KeyWords]
# Ending of Fetching KeyWords in DataBase Table


# Date for freq
today_date = datetime.date.today()
previous_date = today_date - datetime.timedelta(days=1)
# Ending Date for freq

# Accessing Data From Various RSS Feed Source
for url in urls:
    response = requests.get(url)
    br = Browser()
    br.set_handle_robots(False)
    br.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36')]
    br.open(url)
    br._factory.is_html = True
    name = str(br.title())
    name = re.sub(r'[^\w\s]', '', name).replace('   ', ' ').replace('  ', ' ')
    
    if name == 'News':
       name = 'USDOJ'

    if name == 'CDATADark Reading':
       name = 'Dark Reading' 

    if name == 'Geopolitical Cybersecurity Journalist Authority Writer Commentator Consultant Editor':
       name = 'Cybersecurity Journalist Iain Fraser Cybersecurity Geopolitical Journalist Gibraltar'    
       
    feed = fp.parse(url)
    icon_link = feed.entries[0].link
    response = requests.get(icon_link)
    soup = BeautifulSoup(response.content, 'html.parser')
    logo = soup.find('link', rel='icon')
    if logo:
        logos = logo['href']
        # Adding Data For RSS Feed Name and There Icon in DataBase
        add_Name_Icon(name, logos)
    else:
        icons = fi.get(icon_link)
        real_icon_link = icons[0].url
        # Adding Data For RSS Feed Name and There Icon in DataBase
        add_Name_Icon(name, real_icon_link)

    for data in feed.entries:
        Title = [data.title]
        filter_title = [n for n in Title if
             any(m in n for m in search_word)]
        if filter_title:       
          Published = pd.to_datetime(data.published)
          Published_Date = Published.strftime('%Y-%m-%d %H:%M:%S')
          Summary = BeautifulSoup(data.summary, 'lxml').get_text().strip()
          # Adding Data For RSS Feed Name Article's Title, Published Date, Link And Summary in DataBase
          add_database(name, data.title, Published_Date, data.link, Summary)

    # Adding Accepted Article's freq in DataBase
    conn.execute("SELECT publishedDate FROM endpoints_rss_feed_database WHERE feedName= ?", (name,))
    publishedDates_database = conn.fetchall()
    publishedDates = [i[0] for i in publishedDates_database]
    freq_Accepted = sum(1 for publishedDate in publishedDates if previous_date <= datetime.datetime.strptime(publishedDate, "%Y-%m-%d %H:%M:%S").date() <= today_date)
    conn.execute("UPDATE endpoints_rss_feed_name_icon SET feedFrequency_accepted = ? WHERE feedName= ?", (freq_Accepted,name))
    connect.commit()
    # Ending for Adding Accepted Article's freq in DataBase
    
    # Adding Rejected Article's freq in DataBase
    # conn.execute("SELECT publishedDate FROM endpoints_rss_feed_temp WHERE feedName= ?", (name,))
    # publishedDates_database = conn.fetchall()
    # publishedDates = [i[0] for i in publishedDates_database]
    # freq_Rejected = sum(1 for publishedDate in publishedDates if previous_date <= datetime.datetime.strptime(publishedDate, "%Y-%m-%d %H:%M:%S").date() <= today_date)
    # conn.execute("UPDATE endpoints_rss_feed_name_icon SET feedFrequency_reject = ? WHERE feedName= ?", (freq_Rejected,name))
    # connect.commit()    
    # Ending for Adding Rejected Article's freq in DataBase
# Ending For Accessing Data From Various RSS Feed Source

print('DataBase Is Updated!!!!!')
connect.close()
