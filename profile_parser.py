from linkedin_api import Linkedin
from googletrans import Translator
import json
from string import Template
import transliterate


def cv_features(linkedin_page):
  translator = Translator()
  promt_features = dict()

  promt_features['headline'] = linkedin_page.get('headline')
  promt_features['profile_id'] = linkedin_page.get('profile_id')
  promt_features['public_id'] = linkedin_page.get('public_id')
  print(promt_features)
  promt_features['first_name'] = transliterate.translit(linkedin_page.get('firstName'),'ru',reversed=True)
  promt_features['last_name'] = transliterate.translit(linkedin_page.get('lastName'),'ru',reversed=True)
  experience = '\n'
  i = 1
  for jobs in linkedin_page.get('experience'):
    experience = experience + str(i) + ': ' +str(jobs.get('companyName')) + ': ' +'Описание: '+str(jobs.get('description')) + '\n'
    i+=1
  promt_features['experience'] = experience

  return promt_features

def get_profile_info(login,password,linkedin_public_id):
  api = Linkedin(login, password)
  profile = api.get_profile(linkedin_public_id)
  profile_json = json.loads(json.dumps(profile, indent=2))
  return cv_features(profile_json)

def generate_inital_prompt(prfile_info):
  prompt = Template('''
Претендент на позицию:
Имя: $first_name
Текущая должность: $headline
Фамилия: $last_name

Опыт работы: $experience
  ''')
  return prompt.substitute(prfile_info)

# def main():
#   #kirill-timofeev-a57b0a180
#   profile_info = get_profile_info('gekomo97@gmail.com', '!Gg527571997','seemyoon')
#   prompt = generate_inital_prompt(profile_info)
