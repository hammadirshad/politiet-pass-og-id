import os
import time
from datetime import datetime

import sendgrid
from selenium import webdriver
from selenium.webdriver.common.by import By
from sendgrid.helpers.mail import Mail, Email, To, Content


def wait(seconds=2):
  time.sleep(seconds)


def check_appointment(city_map, service, chrome_options,
    limit_date=(datetime.strptime(os.getenv('LIMIT-DATE'),
                                  "%Y-%m-%d") if os.getenv(
        'LIMIT-DATE') else None),
    sendgrid_api_key=os.getenv('SENDGRID_API_KEY'),
    sendgrid_from_email=os.getenv('SENDGRID_FROM_EMAIL'),
    sendgrid_to_email=os.getenv('SENDGRID_TO_EMAIL')):
  earliest_times = []

  for selected_city, city_code in city_map.items():
    start_time = time.time()
    target_url = f"https://pass-og-id.politiet.no/timebestilling/index.html#/preselect/branch/{city_map[selected_city]}?preselectFilters=on"

    print(f"Checking {selected_city} for date limit {limit_date} ...")

    driver = webdriver.Chrome(service=service, options=chrome_options)

    # driver.maximize_window()

    try:
      driver.get(target_url)
      wait(3)

      # Click on "Velg tjeneste"
      # velg_tidspunkt_div = driver.find_element(By.ID, "serviceStepHeading")
      # velg_tidspunkt_div.click()
      # wait(2)

      # Click on "Time til pass og ID-kort"
      button_element = driver.find_element(By.CSS_SELECTOR,
                                           "button[data-v-31fa5ec0]")
      button_element.click()
      wait(2)

      # Click on the plus button to select Antall 1
      plus_button = driver.find_element(By.CLASS_NAME, "plus-btn")
      plus_button.click()
      wait(2)

      # Click on "Velg tidspunkt"
      velg_tidspunkt_div = driver.find_element(By.ID, "dateTimeHeading")
      velg_tidspunkt_div.click()
      wait(5)

      # Get Date from div
      date_div = driver.find_element(By.ID, "selectedDateInfo")
      date_div_bold_vaule = (date_div.find_element(By.TAG_NAME, "b")
                             .text.strip().replace("Tilgjengelig tid den ", ""))

      # Get Time from button
      time_button = driver.find_element(By.ID, "timeButton1")
      time_span_value = (time_button.find_element(By.TAG_NAME, "span")
                         .text.strip())

      message = f"{selected_city} earliest appointment time: {date_div_bold_vaule} {time_span_value}\n"
      print(message)

      try:
        parsed_date = datetime.strptime(date_div_bold_vaule, "%d.%m.%Y")
        if limit_date is None or limit_date > parsed_date:
          email_message = f"{message} \nAppointment URL: {target_url}\n"
          earliest_times.append(email_message)

      except Exception as e1:
        print(f"An error occurred: {e1}")

    except Exception as e:
      print(f"An error occurred: {e}")

    finally:
      # Close the browser after completion
      wait(1)
      driver.quit()
      # end_time = time.time()
      # execution_time = end_time - start_time
      # print(f"Script execution time: {execution_time:.2f} seconds\n")

  if earliest_times and sendgrid_to_email:
    body_content = "\n".join(earliest_times)
    print(body_content)
    subject = "Time til pass og ID-kort"
    from_email = Email(sendgrid_from_email)
    to_email = To(sendgrid_to_email)
    content = Content("text/plain", body_content)
    mail = Mail(from_email, to_email, subject, content)
    sg = sendgrid.SendGridAPIClient(api_key=sendgrid_api_key)
    response = sg.send(mail)

    print()
    print(f"Status Code: {response.status_code}")
    print(f"Response Body: {response.body}")
    print(f"Response Headers: {response.headers}")
