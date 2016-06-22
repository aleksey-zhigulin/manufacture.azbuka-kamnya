# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals

import re

from Queue import Queue
from threading import Thread
import threading

from django.core.management.base import BaseCommand
from django.utils.text import slugify
from django.db.utils import OperationalError
from django.core.files.temp import NamedTemporaryFile
from django.contrib.auth.models import User
from unidecode import unidecode
from urllib2 import urlopen, HTTPError
from bs4 import BeautifulSoup

from filer.management.commands.import_files import FileImporter
from filer.settings import FILER_IS_PUBLIC_DEFAULT
from filer.models.imagemodels import Image
from django.core.files import File

from cms.models.pagemodel import Page

from shop.models.defaults.mapping import ProductPage, ProductImage

from manufacture.models.products.stone import Stone, StoneType
from manufacture.models.products.product import ProductTranslation
from manufacture.models.properties import *
from currencies.models import Currency

from time import sleep

class Command(BaseCommand):

    def handle(self, *args, **options):
        get_stones()

ROOT_URL = 'http://cosmostone.ru'
QUERY = '?material={}&processing={}&color={}&country={}&num_on_page=all'

#Queries
products_query = Queue()
images_query = Queue()
products = {}

TOTAL_PRODUCTS = 0
TOTAL_IMAGES = 0
DONE_PRODUCTS = 0
DONE_IMAGES = 0
MYSQL_SLEEP = 200
NUM_THREADS = 65
NUM_THREADS_IO = 30

# from filer.models.filemodels import File
# from shutil import copyfile
# from manufacture.settings import MEDIA_ROOT
# import os
# for file in File.objects.all():
#     src = os.path.join(MEDIA_ROOT, str(file.file))
#     print (src)
#     dst = os.path.join(MEDIA_ROOT, 'filer_backup', str(file.file))
#     os.makedirs('/'.join(dst.split('/')[:-1]))
#     copyfile(src, dst)

def products_worker():
    global DONE_PRODUCTS, MYSQL_SLEEP, TOTAL_PRODUCTS
    while True:
        arg = products_query.get()
        try:
            process_product(arg)
        except OperationalError:
            print('Thread "%s" Mysql has gone away. Exiting Thread. Active count = %s' % (threading.current_thread().name, threading.active_count()))
            products_query.task_done()
            products_query.put(arg)
            t = Thread(target=products_worker)
            t.daemon = True
            t.start()
            return
        else:
            DONE_PRODUCTS += 1
            products_query.task_done()

def images_worker():
    global DONE_IMAGES, MYSQL_SLEEP, TOTAL_IMAGES
    while True:
        kwargs = images_query.get()
        # while True:
        try:
            process_image(**kwargs)
        except OperationalError:
            print('Thread "%s" Mysql has gone away. Exiting Thread. Active count = %s' % (
            threading.current_thread().name, threading.active_count()))
            images_query.task_done()
            images_query.put(kwargs)
            t = Thread(target=images_worker)
            t.daemon = True
            t.start()
            return
        else:
            DONE_IMAGES += 1
            images_query.task_done()
            # break

def logger_worker():
    while True:
        sleep(1)
        global DONE_PRODUCTS
        print("%s/%s (queried/done) of %s products, %s/%s (queried/done) of %s images, active threads = %s" % (
            products_query.qsize(),
            DONE_PRODUCTS,
            TOTAL_PRODUCTS,
            images_query.qsize(),
            DONE_IMAGES,
            TOTAL_IMAGES,
            threading.active_count()))

def process_image(instance=None, field_name=None, file=None, file_name=None, file_title=None, folder=None):
    instance.image = add_filer_image(
        file=urlopen(file).read(),
        file_name=file_name,
        file_title=file_title,
        folder=folder
    )
    instance.save()

def add_filer_image(file, file_name, file_title, folder, owner='admin'):
    importer = FileImporter()
    folder = importer.get_or_create_folder(folder)
    img_temp = NamedTemporaryFile(delete=True)
    img_temp.write(file)
    file_obj = File(img_temp, name=file_name)
    image, created = Image.objects.get_or_create(
        original_filename=file_title
    )
    image.owner = User.objects.get(username=owner)
    image.file = file_obj
    image.folder = folder
    image.is_public = FILER_IS_PUBLIC_DEFAULT
    image.save()
    img_temp.flush()
    return image

def get_html(url=None):
    while True:
        try:
            return urlopen(url).read()
        except HTTPError:
            print('Error: HTTP Error. Retrying in 5 seconds...')
            sleep(5)

def check_products_exist(url=None):
    soup = BeautifulSoup(get_html(url), 'html.parser')
    div = soup.find("div", id='catalog-products-table')
    return bool(div)

def get_products(url=None, material=None, treatment=None, country=None, color=None):
    soup = BeautifulSoup(get_html(url), 'html.parser')
    div = soup.find("div", id='catalog-products-table')
    products = {}
    if div:
        for table in div.find_all("table"):
            for td in table.find_all("tr")[0].find_all("td"):
                a = td.contents[3]
                name = a['title']
                slug = slugify(unidecode(name))
                products[name] = {
                    'url': a['href'],
                    'thumbnail': ROOT_URL + a.img['src'],
                    'stock': 'Климовск',
                    'slug': slug,
                    'material': material,
                    'treatment': treatment,
                    'country':country,
                    'color': color
                }
    return products

def retrive_products():
    global products, TOTAL_PRODUCTS
    soup = BeautifulSoup(get_html(url = '/'.join([ROOT_URL, 'rus/stock/'])), 'html.parser')
    filter_form = soup.find("form", class_='catalog-filter-form')
    filters = {
        'material': get_filters('material', filter_form),
        'country': get_filters('country', filter_form),
        'treatment': get_filters('processing', filter_form),
        'color': get_filters('color', filter_form),
    }
    products = get_products(url='/'.join([ROOT_URL, 'rus', 'stock', QUERY.format(0, 0, 0, 0)]))
    filtered_products = {}

    for country_name, country_code in filters['country'].iteritems():
        if not check_products_exist(url='/'.join([ROOT_URL, 'rus', 'stock', QUERY.format(
                0, 0, 0, country_code)])): continue
        for color_name, color_code in filters['color'].iteritems():
            if not check_products_exist(url='/'.join([ROOT_URL, 'rus', 'stock', QUERY.format(
                    0, 0, color_code, country_code)])): continue
            for material_name, material_code in filters['material'].iteritems():
                if not check_products_exist(url='/'.join([ROOT_URL, 'rus', 'stock', QUERY.format(
                        material_code, 0, color_code, country_code)])): continue
                for treatment_name, treatment_code in filters['treatment'].iteritems():
                    filtered_products.update(get_products(
                            url='/'.join([ROOT_URL, 'rus', 'stock', QUERY.format(
                                material_code, treatment_code, color_code, country_code)]),
                            material=material_name,
                            country=country_name,
                            treatment=treatment_name,
                            color=color_name
                        )
                    )
                    print('Total products count = %s of %s' % (len(filtered_products), len(products)))
    products.update(filtered_products)
    for order, product_name in enumerate(products.keys()):
        products[product_name]['order'] = order
        products_query.put(product_name)
        TOTAL_PRODUCTS += 1

def process_product(product_name):
    info = products[product_name]
    soup = BeautifulSoup(get_html(ROOT_URL + info['url']), 'html.parser')
    info['groups'] = {}
    size_pattern = re.compile(r'[0-9,.]+ х [0-9,.]+ х [0-9,.]+')
    thickness_pattern = re.compile(r'[0-9] см')
    for group in soup.find_all('tr', class_='group-row'):
        new_group = {}
        for item in soup.find_all('tr', class_='stone-row', rel=group['rel']):
            tds = item.find_all('td')

            name, type, treatment, price = (
                tds[1].a.string,
                tds[2].string,
                tds[3].string,
                tds[9].string,
            )
            img = tds[0].a.img['src'].replace('thumbs', 'images') if tds[0].a.img else ''

            size = size_pattern.search(name)
            if size:
                size = size.group(0).replace(',', '.').replace('х', '✕')

            thickness = thickness_pattern.search(name)
            if thickness:
                thickness = thickness.group(0)

            new_group[name] = {
                'img': ROOT_URL+img,
                'type': unicode(type),
                'treatment': unicode(treatment),
                'price': price,
                'currency': u'EUR',
                'thickness': unicode(thickness),
                'size': unicode(size),
            }

        info['groups'][group.find('td', class_='col-2').span.string] = new_group
    add_product_to_db(product_name)

def get_filters(name, filter_form):
    options_dict = {}
    for option in filter_form.find('select', attrs={'name': name}).find_all('option'):
        if option['value'] != '0':
            options_dict[option.string] = option['value']
    return options_dict

def add_product_to_db(product_name):
    global products, TOTAL_IMAGES
    values = products[product_name]
    slug = values['slug']
    try:
        stone_type = StoneType.objects.get(product_name=product_name)
    except StoneType.DoesNotExist:
        stone_type = StoneType.objects.create(
            product_name=product_name,
            order=values['order'],
            slug=slug
        )

    if values['color']:
        stone_type.stone_color = Color.objects.get_or_create(name=unicode(values['color']))[0]
    else:
        stone_type.stone_color = None
    if values['material']:
        stone_type.stone_rock = Rock.objects.get_or_create(name=unicode(values['material']))[0]
    else:
        stone_type.stone_rock = None
    if values['country']:
        stone_type.stone_country = Country.objects.get_or_create(name=unicode(values['country']))[0]
    else:
        stone_type.stone_country = None
    if values['treatment']:
        stone_type.stone_treatment = Treatment.objects.get_or_create(name=unicode(values['treatment']))[0]
    else:
        stone_type.stone_treatment = None
    stone_type.save()

    # Add description
    # ProductTranslation.objects.get_or_create(
    #     master=stone_type,
    #     description=u'',
    #     language_code='ru'
    # )

    # Add image
    # stone_type.images.clear()
    # ProductImage.objects.get_or_create(
    #     image=add_filer_image(
    #         file=urlopen(values['thumbnail']).read(),
    #         file_name='.'.join([slug, '.jpg']),
    #         file_title=product_name,
    #         folder=['Образцы камня', 'Космос', 'thumbnails']
    #     ),
    #     product=stone_type
    # )

    # Save base stone
    ProductPage.objects.get_or_create(
        page=Page.objects.get(id=30),
        product=stone_type
    )

    # for group, items in values['groups'].iteritems():
    #     for item_number, (name, params) in enumerate(items.iteritems()):
    #         stone_form = Type.objects.get_or_create(name=params['type'])[0]
    #         size = Size.objects.get_or_create(name=params['size'])[0]
    #         thickness = Thickness.objects.get_or_create(name=params['thickness'])[0]
    #         currency = Currency.objects.get_or_create(code=params['currency'])[0]
    #         new_stone, created = Stone.objects.get_or_create(
    #             type=stone_type,
    #             unit_price=params['price'],
    #             currency=currency,
    #             stock=Stock.objects.get_or_create(name=u'Климовск')[0],
    #             stone_size=size,
    #             stone_thickness=thickness,
    #             stone_form=stone_form,
    #         )
    #         new_stone.save()
    #
    #         images_query.put({'instance': new_stone,
    #                           'field_name': 'image',
    #                           'file': params['img'],
    #                           'file_name': '_'.join([slug, group, str(item_number), '.jpg']),
    #                           'file_title': ' '.join([product_name, group, str(item_number)]),
    #                           'folder': ['Образцы камня', 'Космос', product_name]}),
    #         TOTAL_IMAGES += 1

def get_stones():
    retrive_thread = Thread(target=retrive_products)
    retrive_thread.daemon = True
    retrive_thread.start()
    retrive_thread.join()

    logger_thread = Thread(target=logger_worker)
    logger_thread.daemon = True
    logger_thread.start()

    for i in range(NUM_THREADS):
        t = Thread(target=products_worker)
        t.daemon = True
        t.start()

    # for i in range(NUM_THREADS_IO):
    #     t = Thread(target=images_worker)
    #     t.daemon = True
    #     t.start()

    products_query.join()
    # images_query.join()
    logger_thread.join(timeout=0)