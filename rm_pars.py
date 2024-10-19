import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs
import time
from colorama import Fore, init
init()

class Start():
	def __init__(self):
		self.tag = None
		self.url = None
		self.image_count = 1

	def down_num(self, pid_value):
		a = int(input("Сколько вы хотите скачать? \n1.Скачать все \n2.Указать число артов \n"))
		if a == 1:
			pid_value = pid_value
			return pid_value
		if a == 2:
			b = int(input("Введите кол-во артов которые хотите скачать: "))
			pid_value = b
			return pid_value

	def get_url(self, tag, num_page):
		self.tag = tag
		self.num_page = num_page
		self.url = f"https://rm.booru.org/index.php?page=post&s=list&tags={self.tag}&pid={self.num_page}"
		print(f"Поиск по странице {self.url}")
		return self.url

	def get_pid(self, url):
		response = requests.get(url)
		bs = BeautifulSoup(response.text, "lxml")
		last_page_link = bs.find('a', {'alt': 'last page'})
		href = last_page_link.get('href')
		parsed_url = urlparse(href)
		query_params = parse_qs(parsed_url.query)
		a = int(query_params.get('pid', [None])[0])
		pid_value = a + 20
		print(f"Всего страниц: {pid_value // 20} \nАртов примерно {pid_value}")
		return pid_value

	def download_image(self, image_url, folder):
		response = requests.get(image_url)
		if response.status_code == 200:
			bs = BeautifulSoup(response.text, "lxml")
			img_tag = bs.find('img', id='image')
			img_url = img_tag['src']
			image_name = os.path.basename(img_url)
			image_path = os.path.join(folder, image_name)
			with open(image_path, 'wb') as f:
				f.write(response.content)
			print(Fore.GREEN + f"Сохранено: {image_name}")
		else:
			print(Fore.RED + f"Не удалось скачать изображение: {image_url}")

	def download_ing(self, img_url, tag):
		if not os.path.exists(tag):
			os.makedirs(tag)
		response = requests.get(img_url)
		if response.status_code == 200:
			bs = BeautifulSoup(response.text, "lxml")
			img_tag = bs.find('img', id='image')
			if img_tag is not None:
				img_url2 = img_tag['src']
				image_name = f"{tag}_{self.image_count}.jpg"
				image_path = os.path.join(tag, image_name)
				img_response = requests.get(img_url2)
				if img_response.status_code == 200:
					with open(image_path, 'wb') as f:
						f.write(img_response.content)
					print(Fore.GREEN + f"Сохранено: {image_name} в директорию '{tag}'")
					self.image_count += 1
				else:
					print(Fore.RED + f"Не удалось скачать изображение: {img_url2}")
			else:
				print(Fore.RED + f"Изображение не найдено на странице: {img_url}")
		else:
			print(Fore.RED + f"Не удалось получить страницу: {img_url}")




	def pars(self, tag, down_num):
		a = 0
		safe_num = 0
		while safe_num < down_num:
			url = self.get_url(tag, a)
			response = requests.get(url)
			bs = BeautifulSoup(response.text, "lxml")
			posts = bs.find_all('span', {'class': 'thumb'})
			for post in posts:
				if safe_num < down_num:
					post_link = post.a['href']
					img_url = f"https://rm.booru.org/{post_link}"
					response = requests.get(img_url)
					bs = BeautifulSoup(response.text, "lxml")
					img_tag = bs.find('img', id='image')
					if img_tag is not None:
						img_url2 = img_tag['src']
						self.download_ing(img_url, tag)
					safe_num += 1
				else:
					print(Fore.GREEN + f"Загрузка завершена! \nБыло загружено {safe_num} картинок по тэгу {tag}!")
					break
				time.sleep(1)
			a += 20


	def run(self):
		tag = input("Введите тэг: ")
		url = self.get_url(tag, 0)
		pid_value = self.get_pid(url)
		down_num = self.down_num(pid_value)
		self.pars(tag, down_num)



if __name__ == '__main__':
	start_instance = Start()
	start_instance.run()
