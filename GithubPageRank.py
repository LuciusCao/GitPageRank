import re
import requests
import math
import time

def login():
	'''login with my account'''
	url_login = 'https://github.com/login'
	print('enter your login email address')
	user_name = input('')
	print('enter your password')
	user_password = input('')
	data = {'user':user_name,'password':user_password}
	r = requests.get(url_login, data = data)
	return r.cookies

def reg_pro(htmlpage):
	'''Using reg_exp, this function can find the address from github followers/following page 
	and return a list of address of all users related to the input users'''
	address = re.findall(r"(?<=\"follow-list-item\">)\s+<a href=\"/[\w\s\-]+\">",htmlpage)
	u_address = ['' for i in range(len(address))]
	for i in range(len(address)):
		index = re.search(r"/.+\"",address[i]).span()
		u_address[i] = address[i][index[0]+1:index[1]-1]
	return u_address

def get_user_stats(cur_user):
	'''Find the current users followers and followings, 
	return how many pages in followers and followings'''
	url = 'https://github.com/'+cur_user
	user = requests.get(url,cookies=cookies)
	user_homepage = user.text
	user_stats = re.findall(r'(?<=vcard-stat-count\sd-block\">)\d+',user_homepage)
	followers_page_num = math.ceil(int(user_stats[0])/51)
	following_page_num = math.ceil(int(user_stats[2])/51)
	return followers_page_num,following_page_num

def get_user_address(cur_user,ers_or_ing,page_num):
	'''using reg_exp to get the user's followers or following, 
	and the number of its page'''
	if page_num >0:
		temp_list = []
		for i in range(page_num):
			url = 'https://github.com/'+cur_user+'/'+ers_or_ing+'?page='+str(i+1)
			r = requests.get(url,cookies=cookies)
			address = reg_pro(r.text)
			temp_list.extend(address)
	else:
		temp_list = []
	temp_list = list(set(temp_list))
	return temp_list

def one_shot(cur_user):
	'''put everthing together to get a list for a single user'''
	global follow_relation
	ers, ings = get_user_stats(cur_user)
	temp_list_one = []
	a = get_user_address(cur_user,'followers',ers)
	b = get_user_address(cur_user,'following',ings)
	follow_relation[cur_user] = a
	temp_list_one.extend(a)
	temp_list_one.extend(b)
	return list(set(temp_list_one))

if __name__ == '__main__':
	global_user_list = []
	to_scr_user_list = []
	already_user_list = []
	follow_relation = {}
	cookies = login()
	print('Please choose a user to begin with. try nightire here.')
	current_user = input('')
	global_user_list.append(current_user)
	to_scr_user_list.append(current_user)
	start_time = time.time()
	end_time = time.time()
	while int(end_time - start_time) < 3600:
		local_start = time.time()
		current_user = to_scr_user_list.pop()
		one_list = one_shot(current_user)
		already_user_list.append(current_user)
		global_user_list.extend(one_list)
		global_user_list = list(set(global_user_list))
		add_to_scr = [i for i in one_list if i not in already_user_list]
		to_scr_user_list.extend(add_to_scr)
		to_scr_user_list = list(set(to_scr_user_list))
		end_time = time.time()
		print(current_user+':'+str(int(end_time - local_start)))
	print(int(time.time()-start_time))
