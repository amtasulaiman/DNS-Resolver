
import datetime
import sys
import time
import dns.query

start = time. time()
try:
    web = sys.argv[1]   # stores the argument from terminal
except:
    print("Invalid argument for dig")
web = dns.name.from_text(web)
# making a dns query for NS type
request = dns.message.make_query(web, 'A')
file = open("mydig_output.txt", "a")
file.write("\nQUESTION SECTION:")
file.write(str(request.question.__getitem__(0)))

# displaying the query's first element which is the Question
print("\nQUESTION SECTION:")
print(request.question.__getitem__(0))

# sending the query to the root server via UDP
result = dns.query.udp(request, '198.41.0.4')
i = 0 # counter for retrieving A record ip only
# while successful answer isn't achieved, keep going down the chain
while not result.answer:
    # if the entry has A record name then get the ip for the following query
    if str(result.additional[i]).__contains__(' A '):
        ip = str(result.additional[i][0])
        ip = ip.encode()

    # making the query for A record and contacting the ip received via prev query
        request = dns.message.make_query(web, 'A')
        result = dns.query.udp(request, ip)
    else: # increment down the additional if a valid ip isn't retrieved
        i = i + 1

# successful answer is obtained, store it
if result.answer:
    result = result.answer[0]

# displaying the final Answer
print("\nANSWER SECTION: ")
print(str(result))
# writing to the file the answer of final query
file.write("\n")
file.write("ANSWER SECTION: ")
file.write(str(result))
# ending the time and displaying appropriate time and date after calculation
end = time. time()
calc = end - start
calc1 = round(calc, 2)*1000
print("\nQuery time:", calc1, "msec")
file.write('\nQuery time:' + repr(calc1) + 'seconds')
datetime_object = datetime.datetime.now()
print("WHEN: ", datetime_object)
datetime_object = str(datetime_object)
file.write('\nWHEN: ' + repr(datetime_object))
# parsing the result to a string so that size of packet can be obtained
response = str(result)
print("MSG SIZE rcvd: ", len(response))
file.write('\nMSG SIZE rcvd: ' + repr(len(response)))

file.close()
