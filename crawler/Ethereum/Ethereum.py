import requests
from bs4 import BeautifulSoup

## Open input file
in_fp = open('input.txt', 'r')
line = in_fp.readline()
line = line.strip('\n')
find_path = line
count = 1

## Open output file
out_fp = open('output.txt', 'w')

while line:
	addr = 'https://www.blockchain.com/eth/address/' + line + '?view=standard'
	r = requests.get(addr)
	print(r)
	soup = BeautifulSoup(r.text, 'html.parser')
	# now data
	now_hash = soup.find_all('div', class_ = 'sc-1enh6xt-0 kiseLw')
	for nh in now_hash:
		name = nh.find('span', class_ = 'sc-1ryi78w-0 cILyoi sc-16b9dsl-1 ZwupP sc-1n72lkw-0 ebXUGH')
		if name.string != 'Hash':
			out_fp.write(name.string)
			out_fp.write(': ')
			name = nh.find('span', class_ = 'sc-1ryi78w-0 cILyoi sc-16b9dsl-1 ZwupP u3ufsr-0 eQTRKC')
			out_fp.write(name.string)
			out_fp.write('\n')
		else:
			now_hash = nh.find('span', class_ = 'sc-1ryi78w-0 cILyoi sc-16b9dsl-1 ZwupP u3ufsr-0 eQTRKC').string
	# oldest data
	find_date = soup.find_all('div', class_ = 'odi4cq-0 gVJVZs')
	oldest_data = ''
	oldest_addr = ''
	tmp_time = ''
	yes = False
	for od in find_date:
		name = od.find('span', class_ = 'sc-1ryi78w-0 cILyoi sc-16b9dsl-1 ZwupP sc-1n72lkw-0 ebXUGH')
		if name.string == 'Date':
			tmp_time = 'Date: '
			name_data = od.find('span', class_ = 'sc-1ryi78w-0 cILyoi sc-16b9dsl-1 ZwupP u3ufsr-0 eQTRKC')
			tmp_time = tmp_time + name_data.string + '\n'
			print(tmp_time)
		elif name.string == 'From':
			name_data = od.find('a', class_ = 'sc-1r996ns-0 fLwyDF sc-1tbyx6t-1 kCGMTY iklhnl-0 eEewhk')
			print(name.string)
			print(name_data.string)
			print(line)
			if name_data.string.lower() == line.lower():
				oldest_data = tmp_time
				yes = True
			else:
				yes = False
		elif name.string == 'To' and yes:
			name_data = od.find('a', class_ = 'sc-1r996ns-0 fLwyDF sc-1tbyx6t-1 kCGMTY iklhnl-0 eEewhk')
			oldest_data = oldest_data + 'To: ' + name_data.string + '\n'
			oldest_addr = name_data.string
		elif name.string == 'Amount' and yes:
			name_data = od.find('span', class_ = 'sc-1ryi78w-0 cILyoi sc-16b9dsl-1 ZwupP u3ufsr-0 eQTRKC sc-85fclk-0 fhjukF')
			oldest_data = oldest_data + 'Amount: ' + name_data.string	
	if oldest_addr != '' and count != 4:
		find_path = find_path + ' -> ' + oldest_addr
		out_fp.write(oldest_data)
		out_fp.write('\n')
		out_fp.write('--------------------------------------------------------------------------\n')
		line = oldest_addr
		count = count + 1
	elif oldest_addr != '' and count == 4:
		out_fp.write(oldest_data)
		out_fp.write('\n')
		out_fp.write('--------------------------------------------------------------------------\n')
		out_fp.write(find_path)
		out_fp.write('\n')
		out_fp.write('--------------------------------------------------------------------------\n')
		line = in_fp.readline()
		line = line.strip('\n')
		find_path = line
		count = 1
	else:
		out_fp.write('--------------------------------------------------------------------------\n')
		out_fp.write(find_path)
		out_fp.write('\n')
		out_fp.write('--------------------------------------------------------------------------\n')
		line = in_fp.readline()
		line = line.strip('\n')
		find_path = line
		count = 1


in_fp.close()
out_fp.close()