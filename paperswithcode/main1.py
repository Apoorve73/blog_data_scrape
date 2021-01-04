from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import time
import json

def get_structure(path):
	data = {}
	last = {}
	start = time.time()

	data['site_info']= list()
	options = webdriver.ChromeOptions()
	# driver = webdriver.Chrome(executable_path=path, options=options)
	
	base_url = 'https://paperswithcode.com/'

	# capa["pageLoadStrategy"] = "none"

	driver = webdriver.Chrome(executable_path=path, options=options)
	wait = WebDriverWait(driver, 30)

	driver.get(base_url + 'sota')
	
	time.sleep(5)

	try:
		try:
			level1 = driver.find_elements_by_class_name('task-group-title')
		except  Exception as e:
			print(f'task-group-title\n{e}')
		try:
			level1_names = [i.text for i in level1]
		except Exception as e:
			print(f'lvl1_name\n{e}')

		for place1, level1_name in enumerate(level1_names):
			print(f'\n{place1+1}/{len(level1_names)}')
			print(f'{level1_name}')

			try:
				data['site_info'].append({
					level1_name: {}
				})
			except Exception as e:
				print(f'lvl1_add{e}')

			try:
				driver.get(base_url + 'area/' + level1_name.lower().replace(' ', '-'))
				time.sleep(10)
			except Exception as e:
				print(f'going to lvl2\n{e}')

			try:
				level2 = driver.find_elements_by_tag_name('h4')
			except  Exception as e:
				print(f'h4\n{e}')
			try:
				level2_names = [i.text for i in level2]
			except Exception as e:
				print(f'lvl2_name\n{e}')

			for place2, level2_name in enumerate(level2_names):
				print(f'{place1+1}/{len(level1_names)}-->{place2+1}/{len(level2_names)}')
				print(f'{level1_name}-->{level2_name}')

				try:
					temp = {level2_name: {}}
					data['site_info'][place1][level1_name].update(temp)
				except Exception as e:
					print(f'lvl2_add{e}')

				try:
					driver.get(base_url + 'area/' + level1_name.lower().replace(' ', '-') + '/' + level2_name.lower().replace(' ', '-'))
					time.sleep(5)
				except Exception as e:
					print(f'going to lvl3\n{e}')

				try:
					level3 = driver.find_elements_by_class_name('card')
				except  Exception as e:
					print(f'card\n{e}')
				try:
					level3_names = [i.find_element_by_class_name('card-title').text for i in level3]
				except Exception as e:
					print(f'lvl3_name\n{e}')
				try:
					level3_links = [i.find_element_by_tag_name('a').get_attribute('href') for i in level3]
				except Exception as e:
					print(f'lvl3_links\n{e}')

				for place3, level3_link in enumerate(level3_links):

					try:
						driver.get(level3_link)
						time.sleep(5)
					except Exception as e:
						print(f'getting finals\n{e}')

					# try:
					# 	bread = driver.find_element_by_class_name('general-breadcrumb').text
					# except  Exception as e:
					# 	print('breadcrumb')

					try:
						name_class = driver.find_element_by_class_name("artefact-information")
						name = name_class.find_element_by_tag_name('h1').text

					except Exception as e:
						print('name')

					try:
						link = driver.current_url
					except  Exception as e:
						print('link')
					print(f'{place1+1}/{len(level1_names)}-->{place2+1}/{len(level2_names)}-->{place3+1}/{len(level3_links)}')
					print(f'{level1_name}-->{level2_name}-->{name}')

					try:
						temp = {name: {"link": link}}
						data['site_info'][place1][level1_name][level2_name].update(temp)
						seconds = time.time() - start
						m, s = divmod(seconds, 60)
						h, m = divmod(m, 60)
						print("\t%d:%02d:%02d" % (h, m, s))
						print('----------')
					except Exception as e:
						print(f'final_adding\n{e}')


		with open('site_info_1.json', 'w') as outfile:
			json.dump(data, outfile)
			
	except  Exception as e:
		pass

	driver.quit()


get_structure('../chromedriver')
