import re
import os
import time
import sys
import pandas as pd
import uuid
import datetime
from regex import E
from sqlalchemy import create_engine
import multiprocessing

# from .models import PermitDataOther

from fake_useragent import UserAgent

from bs4 import BeautifulSoup
from itertools import repeat

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from selenium.webdriver.chrome.options import Options as Chrome_Options

from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.support.select import Select

# BMT_DATA_FOLDER = os.getenv('BMT_DATA_FOLDER')
BMT_DATA_FOLDER = '/Users/rapple2018/OneDrive - NA/bmt-specific-cases/'
HVAC_DATA_FOLDER = BMT_DATA_FOLDER + 'hvac/data/'

#Function that creates a driver that automatically saves certain file extensions
#in a specific folder
def driver_settings_chrome(download_folder, options_bool=False):
    chrome_options = Chrome_Options()

    prefs = {"profile.default_content_settings.popups": 0,
                 "download.default_directory": download_folder, # IMPORTANT - ENDING SLASH V IMPORTANT
                 "download.prompt_for_download": False,
                 "download.directory_upgrade": True,
                 "safebrowsing.enabled": True,
                 "plugins.always_open_pdf_externally": True}
    chrome_options.add_experimental_option("prefs", prefs)

    #Enable this on the server, disable on local machines
    # chrome_options.binary_location = "/usr/bin/chromium-browser"
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')

    ua = UserAgent()
    userAgent = ua.random
    chrome_options.add_argument(f'user-agent={userAgent}')

    if options_bool:
        chrome_options.headless=True

    driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
    driver.set_window_size(1920, 1080)
    # driver = uc.Chrome(options=chrome_options)

    print("open browser, current session is {}".format(driver.session_id))

    return driver

'''
    This function makes the code more readable
    Condenses find element logic into fewer characters
    params:
        timeout - timeout after N seconds
        xpath - xpath to search for
'''
def find_ele(driver, timeout, xpath):
    output = WebDriverWait(driver, timeout).until(EC.presence_of_all_elements_located((By.XPATH, xpath)))

    # If there is only one element, do not return a list
    if len(output)==1:
        output = output[0]

    return output

def find_ele_next_sib_text(driver, timeout, xpath):
    try:
        return find_ele(driver, timeout, xpath).find_element_by_xpath('./following-sibling::div').text

    except:
        return '_'

COUNTY_NAME = "pinellas"
COUNTY_WEBSITE = 'https://aca-prod.accela.com/PINELLAS/Cap/CapHome.aspx?module=Building&TabName=Building'

def search_prep(driver, start_date_val, end_date_val, license_type=None, license_num=None):
    LICENSE_NUMBER_XPATH = '//*[contains(@id, "ctl00_PlaceHolderMain_generalSearchForm_txtGSLicenseNumber")]/input'
    START_DATE_XPATH = '//*[@id="ctl00_PlaceHolderMain_generalSearchForm_txtGSStartDate"]'
    END_DATE_XPATH = '//*[@id="ctl00_PlaceHolderMain_generalSearchForm_txtGSEndDate"]'
    NEW_SEARCH_CONTAINER = '//a[@id="ctl00_PlaceHolderMain_btnNewSearch"]'
    SELECT_LICENSE_TYPE = '//select[@id="ctl00_PlaceHolderMain_generalSearchForm_ddlGSLicenseType"]'

    driver.get(COUNTY_WEBSITE)

    if license_type is not None:
        sel_license_type = Select(find_ele(driver, 10, SELECT_LICENSE_TYPE))
        sel_license_type.select_by_value(license_type)

    if license_num is not None:
        find_ele(driver, 10, LICENSE_NUMBER_XPATH).send_keys(license_num)

    start_date = find_ele(driver, 10, START_DATE_XPATH)
    start_date.send_keys(Keys.COMMAND+'a')
    start_date.send_keys(Keys.DELETE)
    start_date.send_keys(start_date_val)

    end_date = find_ele(driver, 10, END_DATE_XPATH)
    end_date.send_keys(Keys.COMMAND+'a')
    end_date.send_keys(Keys.DELETE)
    end_date.send_keys(end_date_val)

    find_ele(driver, 10, START_DATE_XPATH)

    find_ele(driver, 10, NEW_SEARCH_CONTAINER).click()

def find_record(driver, record_num):
    LICENSE_NUMBER_XPATH = '//*[@id="ctl00_PlaceHolderMain_generalSearchForm_txtGSPermitNumber"]'
    START_DATE_XPATH = '//*[@id="ctl00_PlaceHolderMain_generalSearchForm_txtGSStartDate"]'
    END_DATE_XPATH = '//*[@id="ctl00_PlaceHolderMain_generalSearchForm_txtGSEndDate"]'
    NEW_SEARCH_CONTAINER = '//a[@id="ctl00_PlaceHolderMain_btnNewSearch"]'

    driver.get(COUNTY_WEBSITE)

    find_ele(driver, 10, LICENSE_NUMBER_XPATH).send_keys(record_num)

    start_date = find_ele(driver, 10, START_DATE_XPATH)
    start_date.send_keys(Keys.COMMAND+'a')
    start_date.send_keys(Keys.DELETE)
    start_date.send_keys('01/01/2000')

    end_date = find_ele(driver, 10, END_DATE_XPATH)
    end_date.send_keys(Keys.COMMAND+'a')
    end_date.send_keys(Keys.DELETE)
    end_date.send_keys('12/31/2025')

    find_ele(driver, 10, START_DATE_XPATH)

    find_ele(driver, 10, NEW_SEARCH_CONTAINER).click()

def scrape_licensed_professionals(driver, record_num, index_val):
    TBL_ROWS_XPATH = '//table[@id="tbl_licensedps"]/tbody/tr'
    OTHER_PROFESSIONALS_XPATH = '//*[@id="link_licenseProfessional"]'
    
    try:
        find_ele(driver, 5, OTHER_PROFESSIONALS_XPATH).click()
    except:
        print('No other professionals!')

    try:
        tbl_rows = find_ele(driver, 10, TBL_ROWS_XPATH)
        if not isinstance(tbl_rows, list):
            tbl_rows = [tbl_rows]

        keep_records = [0]
        if len(tbl_rows) > 3:
            keep_records.extend(list(range(3, len(tbl_rows))))

        tbl_rows = [tbl_rows[x] for x in keep_records]
        output = []
        for x in tbl_rows:
            data = {
                'RECORD_NUMBER': record_num,
                'PROFESSIONALS' : x.find_element_by_xpath('./td[2]').text
            }
            data = pd.DataFrame([data])
            output.append(data)
        
        output = pd.concat(output)
    except:
        print('~~Professionals Scrape Failed!~~')
        output = {
            'RECORD_NUMBER': record_num,
            'PROFESSIONALS': '_'
        }
        output = pd.DataFrame([output])

    old_cols = list(output.columns)
    new_cols = ['id']
    new_cols.extend(old_cols)
    
    output['id'] = index_val
    output = output[new_cols]
    output['LOAD_DATE_TIME'] = datetime.datetime.now()
    print(output)

    return output


def scrape_record_other_details_col_names(driver):
    MORE_DETAILS_XPATH = '//a[@id="lnkMoreDetail"]'
    APP_INFO_XPATH = '//*[@id="lnkASI"]'
    COL_NAMES_XPATH = '//div[contains(@class, "MoreDetail_ItemColASI") and contains(@class, "MoreDetail_ItemCol1")]/span'
    find_ele(driver, 30, MORE_DETAILS_XPATH).click()
    find_ele(driver, 2, APP_INFO_XPATH).click()
    time.sleep(5)
    cols = find_ele(driver, 10, COL_NAMES_XPATH)
    cols = [x.text + '\n' for x in cols]
    for col in cols:
        with open('other_details_col_names.txt', 'a') as f:
            f.write(col)

def scrape_record_other_details(driver, record_num, index_val):
    MORE_DETAILS_XPATH = '//a[@id="lnkMoreDetail"]'
    ADD_INFO_XPATH = '//*[@id="lnkAddtional"]'
    APP_INFO_XPATH = '//*[@id="lnkASI"]'
    PARCEL_INFO_XPATH = '//*[@id="lnkParcelList"]'
    JOB_VALUE_XPATH = '//*[@id="ctl00_PlaceHolderMain_PermitDetailList1_tdADIContent"]/div/div/span[2]'
    APP_INFO_DATA_XPATH = '//tr[@id="trASIList"]/td[1]/div[1]/'

    # CONSTRUCTION_TYPE_XPATH = APP_INFO_DATA_XPATH + 'div[3]/span[1]'
    # PERMIT_TYPE_XPATH = APP_INFO_DATA_XPATH + 'div[4]/span[1]'
    # SUBPERMIT_TYPE_XPATH = APP_INFO_DATA_XPATH + 'div[5]/span[1]'
    # CONSTRUCTION_VALUE_XPATH = APP_INFO_DATA_XPATH + 'div[6]/span[1]'
    # WORK_AREA_XPATH = APP_INFO_DATA_XPATH + 'div[7]/span[1]'

    CONSTRUCTION_TYPE_XPATH = '//*[contains(text(), "Construction Type") and contains(text(), "Description")]' #/following-sibling::/div/span
    PERMIT_TYPE_XPATH = '//*[contains(text(), "Permit Type")]/parent::div'
    SUBPERMIT_TYPE_XPATH = '//*[contains(text(), "Sub Type")]/parent::div'
    CONSTRUCTION_VALUE_XPATH = '//*[contains(text(), "Value of Construction")]/parent::div'
    WORK_AREA_XPATH = '//*[contains(text(), "Work Area")]/parent::div'
    AC_UNIT_MAKE_XPATH = '//*[contains(text(), "AC") and contains(text(), "Unit Make")]/parent::div'
    AC_UNIT_MODEL_XPATH = '//*[contains(text(), "AC") and contains(text(), "Unit Model")]/parent::div'
    ADDITIONAL_COSTS_XPATH = '//*[contains(text(), "Cost of Addition")]/parent::div'
    EXISTING_STRUCTURE_ADDITIONS_XPATH = '//*[contains(text(), "Existing Structure Addition")]/parent::div'
    NUM_ROOF_AC_UNITS_XPATH = '//*[contains(text(), "roof AC units to remove and reinstall")]/parent::div'
    RES_OR_COMM_XPATH = '//span[contains(text(), "Residential or Commercial Construction")]/parent::div'

    PARCEL_NUM_XPATH = '//tr[@id="trParcelList"]/td/div[1]/div[1]/div[1]'

    find_ele(driver, 30, MORE_DETAILS_XPATH).click()

    try:
        find_ele(driver, 2, ADD_INFO_XPATH).click()
        job_value = find_ele(driver, 2, JOB_VALUE_XPATH).text

    except:
        job_value = '_'

    try:
        find_ele(driver, 2, APP_INFO_XPATH).click()

        construction_type = find_ele_next_sib_text(driver, 2, CONSTRUCTION_TYPE_XPATH)
        permit_type = find_ele_next_sib_text(driver, 2, PERMIT_TYPE_XPATH)
        subpermit_type = find_ele_next_sib_text(driver, 2, SUBPERMIT_TYPE_XPATH)
        construction_value = find_ele_next_sib_text(driver, 2, CONSTRUCTION_VALUE_XPATH)
        work_area = find_ele_next_sib_text(driver, 2, WORK_AREA_XPATH)
        ac_unit_make = find_ele_next_sib_text(driver, 2, AC_UNIT_MAKE_XPATH)
        ac_unit_model = find_ele_next_sib_text(driver, 2, AC_UNIT_MODEL_XPATH)
        additional_costs = find_ele_next_sib_text(driver, 2, ADDITIONAL_COSTS_XPATH)
        existing_structures_additions = find_ele_next_sib_text(driver, 2, EXISTING_STRUCTURE_ADDITIONS_XPATH)
        num_roof_ac_units = find_ele_next_sib_text(driver, 2, NUM_ROOF_AC_UNITS_XPATH)
        res_or_comm = find_ele_next_sib_text(driver, 5, RES_OR_COMM_XPATH)
        
    except:
        construction_type = '_'
        permit_type = '_'
        subpermit_type = '_'
        construction_value = '_'
        work_area = '_'
        ac_unit_make = '_'
        ac_unit_model = '_'
        additional_costs = '_'
        existing_structures_additions = '_'
        num_roof_ac_units = '_'
        res_or_comm = '_'

    try:
        find_ele(driver, 2, PARCEL_INFO_XPATH).click()
        parcel_num = find_ele(driver, 2, PARCEL_NUM_XPATH).text

    except:
        parcel_num = '_'

    output = {
            'RECORD_NUMBER': record_num,
            'JOB_VALUE': job_value,
            'CONSTRUCTION_TYPE': construction_type,
            'PERMIT_TYPE': permit_type,
            'SUBPERMIT_TYPE': subpermit_type,
            'CONSTRUCTION_VALUE': construction_value,
            'WORK_AREA': work_area,
            'PARCEL_NUMBER': parcel_num,
            'AC_UNIT_MAKE': ac_unit_make,
            'AC_UNIT_MODEL': ac_unit_model,
            'ADDITIONAL_COSTS': additional_costs,
            'EXISTING_STRUCTURE_ADDITIONS': existing_structures_additions,
            'NUM_ROOF_AC_UNITS': num_roof_ac_units,
            'RES_OR_COMM': res_or_comm
            }

    print(output)

    output = pd.DataFrame([output])
    old_cols = list(output.columns)
    new_cols = ['id']
    new_cols.extend(old_cols)
    output['id'] = index_val
    output = output[new_cols]
    output['LOAD_DATE_TIME'] = datetime.datetime.now()

    return output

def scrape_app_info(driver, record):
    pass

# def upload_record_other_details(details):
#     record = PermitDataOther(EMAIL=email, NAME=name)
#     record.save()
#     print('it works!')

def get_tbl(driver, license_type, index_val):
    TBL_XPATH = '//table[@id="ctl00_PlaceHolderMain_dgvPermitList_gdvPermitList"]'

    tbl = find_ele(driver, 10, TBL_XPATH).get_attribute('outerHTML')
    tbl = pd.read_html(tbl)[0]

    tbl.columns = tbl.iloc[2]

    tbl = tbl[[x for x in tbl.columns.values if str(x)!='nan']]
    tbl.columns = [re.sub(' ', '_', x.upper()) for x in tbl.columns.values]

    tbl = tbl.iloc[3:(tbl.shape[0]-2)]
    tbl['DATE'].fillna("12/31/9999", inplace=True)
    tbl['EXPIRATION_DATE'].fillna("12/31/9999", inplace=True)
    tbl.fillna("", inplace=True)

    col_names = tbl.columns
    new_col_names = ['id', 'COUNTY']
    new_col_names.extend(col_names)

    tbl['id'] = [x for x in range(index_val, index_val + tbl.shape[0])]
    tbl['COUNTY'] = 'pinellas'

    tbl = tbl[new_col_names]

    tbl['LOAD_DATE_TIME'] = datetime.datetime.now()

    tbl['LICENSE_TYPE'] = license_type


    return tbl

def engine_fn(user, pw, host, port, db):
    type = 'postgresql+psycopg2'

    string = type + "://" + str(user) + \
                ":" + str(pw) + '@' + str(host) + ":" + str(port) + "/" + db

    engine = create_engine(string)

    return engine

def do_everything(record, index_val):
    try:
        driver = driver_settings_chrome(HVAC_DATA_FOLDER, True)
        driver.maximize_window()
        find_record(driver, record)
        professionals = scrape_licensed_professionals(driver, record, index_val)
        details = scrape_record_other_details(driver, record, index_val)

        # professionals.to_sql('data_permitdataotherprofessionals', engine, if_exists='append', index=False)
        prof_xpt_file = HVAC_DATA_FOLDER + 'pinellas/data_permitdataotherprofessionals_' + record + '.csv'
        professionals.to_csv(prof_xpt_file, index=None, sep='~')

        # details.to_sql('data_permitdataotherdetails', engine, if_exists='append', index=False)
        details_xpt_file = HVAC_DATA_FOLDER + 'pinellas/data_permitdataotherdetails_' + record + '.csv'
        details.to_csv(details_xpt_file, index=None, sep='~')
        driver.quit()

    except:
        print('Failed!')

def do_everything_loop(record_list, index_list):
    for i in range(0, len(record_list)):
        print(record_list[i], index_list[i])
        do_everything(record_list[i], index_list[i])

def sublists_maker(main_list, num_parallel_procs):
    items_per_list = int(len(main_list) / num_parallel_procs if len(main_list) > num_parallel_procs else num_parallel_procs)
    sublist_ranges = []

    if len(main_list) == num_parallel_procs:
        for x in range(0, num_parallel_procs):
            sublist_ranges.append(main_list[x:(x+1)])
    else:
        for x in range(0, num_parallel_procs):
            start = items_per_list*x
            if x == (num_parallel_procs-1):
                stop = len(main_list)+1
            else:
                stop = items_per_list*(x+1)

            sublist_ranges.append(main_list[start:stop])

    sublist_ranges = [x for x in sublist_ranges if len(x)>0]

    return(sublist_ranges)

def upload_csvs_to_sql(folder, file_flag, engine, tbl):
    files = [folder + x for x in os.listdir(folder) if file_flag in x]
    data = []
    for x in files:
        try:
            data.append(pd.read_csv(x, sep='~'))
        except:
            print('Err with file:\t' + x)

    data = pd.concat(data)

    index_val = pd.read_sql('SELECT MAX(id) as index_val FROM ' + tbl + ';', engine)
    index_val = index_val['index_val'][0]
    index_val += 1
    index_range = range(index_val, index_val+data.shape[0])
    data['id'] = index_range
    data.to_sql(tbl, engine, if_exists='append', index=False)

    for file in files:
        basename = os.path.basename(file)
        os.rename(folder + basename, folder + 'already_loaded/' + basename)
    
    print('# of ' + file_flag + ' files uploaded to SQL:\t' + str(len(files)))

if __name__ == '__main__':
    engine = engine_fn('postgres', 'postgres', 'localhost', '5433', 'bmt_sales_automation')
    if sys.argv[1]=='find_records':
        index_val = pd.read_sql('SELECT MAX(id) as index_val FROM public.data_permitdata;', engine)
        index_val = index_val['index_val'][0]
        index_val += 1

        start_date = pd.read_sql('SELECT MAX("DATE") as start_date FROM public.data_permitdata;', engine)
        start_date = start_date['start_date'][0]
        start_date = str(start_date)
        start_date = start_date.split('-')
        start_date = start_date[1] + '/' + start_date[2] + '/' + start_date[0]

        end_date = pd.read_sql('SELECT MIN("DATE") as end_date FROM public.data_permitdata;', engine)
        end_date = end_date['end_date'][0]
        end_date = str(end_date)
        end_date = end_date.split('-')
        end_date = end_date[1] + '/' + end_date[2] + '/' + end_date[0]
        
        start_date = '01/01/2022'
        end_date = '12/31/2022'

        print('Started scraping dates from ' + start_date + ' to ' + end_date)

        driver = driver_settings_chrome(HVAC_DATA_FOLDER, True)
        license_type = 'Air Cond A Contractor'
        search_prep(driver, start_date, end_date, license_type)
        
        while True:
            # try:
            WebDriverWait(driver, 30).until(EC.invisibility_of_element_located((By.XPATH, '//*[@id="divLoadingTemplate"]')))

            tbl = get_tbl(driver, license_type, index_val)
            tbl.to_sql('data_permitdata', engine, if_exists='append', index=False)
            index_val += 10

            break_counter = 0
            while True:
                if break_counter > 3:
                    break

                else:
                    try:
                        find_ele(driver, 20, '//*[@class="aca_pagination_td aca_pagination_PrevNext"][2]/a').click()
                        break
                    except:
                        time.sleep(1)
                        break_counter += 1

            if break_counter > 3:
                break

            print('Successfully loaded!')
        
        print('Finished scraping dates from ' + start_date + ' to ' + end_date)

    if sys.argv[1]=='scrape_single_record':
        parallel_procs = 8
        index_val = pd.read_sql('SELECT MAX(id) as index_val FROM public.data_permitdataotherdetails;', engine)
        index_val = index_val['index_val'][0]
        index_val = index_val + 1

        # record_num_sql = 'SELECT distinct "RECORD_NUMBER" FROM public.data_permitdata where "DATE" < ' + "'01/01/2009';"
        record_num_sql = 'SELECT distinct public.data_permitdata."RECORD_NUMBER" FROM public.data_permitdata \
                left join public.data_permitdataotherdetails \
                on public.data_permitdata."RECORD_NUMBER" = public.data_permitdataotherdetails."RECORD_NUMBER" \
                left join public.data_permitdataotherprofessionals \
                on public.data_permitdata."RECORD_NUMBER" = public.data_permitdataotherprofessionals."RECORD_NUMBER" \
                where "DATE" > ' + "'12/31/2020'" + \
                'and ("CONSTRUCTION_VALUE" is null or "PROFESSIONALS" is null);'
        record_nums = pd.read_sql(record_num_sql, engine)
        record_nums = list(record_nums['RECORD_NUMBER'])
        print('# of records to scrape:\t' + str(len(record_nums)))

        # record_nums = ['EBP-21-13724']

        # for record in record_nums[(index_val + 1):]:
        index_list = range((index_val + 1), (len(record_nums)+index_val+1))
        print('# of indices:\t' + str(len(index_list)))
        parallel_procs = min([len(record_nums), parallel_procs])
        record_nums = sublists_maker(record_nums, parallel_procs)
        index_list = sublists_maker(index_list, parallel_procs)
        pool = multiprocessing.Pool(processes=parallel_procs)
        pool.starmap(do_everything_loop, zip(record_nums, index_list))

    if sys.argv[1]=='upload_csvs_to_sql':
        upload_csvs_to_sql(HVAC_DATA_FOLDER + 'pinellas/', 'data_permitdataotherdetails', engine, 'data_permitdataotherdetails')
        upload_csvs_to_sql(HVAC_DATA_FOLDER + 'pinellas/', 'data_permitdataotherprofessionals', engine, 'data_permitdataotherprofessionals')