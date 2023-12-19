import requests
import json
from requests_futures.sessions import FuturesSession
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from requests.exceptions import RequestException

roblox_cookie = {".ROBLOSECURITY": "_|WARNING:-DO-NOT-SHARE-THIS.--Sharing-this-will-allow-someone-to-log-in-as-you-and-to-steal-your-ROBUX-and-items.|_E333931CDB607018A043A5C2B07C2BE818975EFEF7B72189A9A1E196EACE38F8C390605AC10B9664108EF009FDD61EDB9ADF764D93957067FBA95A0080D715B750B036594277BACA73F3168A7B31F049347A4E6ED9C0973F11FE9FBE428CDB7F24184D783046C8F482AE909C8B1FC2B6F45A104DE47994ED16AB7CBD586BFE9002D929534CAC2EC2EE75A4B04C39B3D601316D9D5FBA69A858CC35AD221BD49D7B55E61615F21710B2BF0A78629932774DB87BB9652299DE7180172E1D7E44E0CBBE3A773EB98684F0EAD96A6EB191C46860C709882D86A01511EB3BDDA02AB84C7A7BFA2AE6E1B507932934139A22753DE0AE61E06A8F42680B7980DFB747B8C8067816131DD5F5EA3A798387D75576B3BC148C200AAF70CEDE308E16029ACB06EEED544A4807EA2E273ABBD3C34EB729B5E2951947DC72300B1172BB853801C66D4C50FCE2FA266DC401B6EA3D55FAA1FF04BFAE9940F6B67E837511C4DE2918016691E32C201C346F7D4CF9B27CECF4ACFD4767B4A0586D379D12605BFDCE99A93F50B1B7962A5EDFA3DB45832C383EDA9003EA66650FA5728E8D406232D244D221E192763F6D3D4B8B8E6F81E7ACC6FCED28200BA8BEB94230D7B3CF27AA1E6489FE06FC16065E5E8E0852D714FC05F0E7BC31001A727022008DEAB37F68968840282C744D09F6792B3D54DDB35D91E7E4332628C947EFEE266E4AC0D75F6B7C5D932EB00A8A049D3C56411EEB209D28F9B78C8B9C4B20CC8341C7644985B754F371355965052429D788859A0841CFD8DFD6EAA02AF75BF8C7B83AF263F78F19E955EF33AAF7D68F72B40105A0714BCDBC9086644E114FA721DC94BE1C3EB76D6EE5B932CA6B90FE7CBCABC66508889F6E8AC593C65D30B34B50C08BFF57C60B7D4A3DCEAAED47D95F1DA873B0BADD4F8123C975694A527BDE9B1DF1C14C2FC5AA425C7EA916FAFC5685C93BA41548F40E78EDF2F0BE1A3DD3E36A2B84ACD8A1D2F7BE8C5A75BFDA8F0D03C59333A843E8B99C22599B3FEAA5DAD7B12DD75F428D4DCEA77E75103B565D4546E847B4F79FC8"}
def clothings(id):
  clothings = 0
  session = FuturesSession()
  retries = Retry(total=5, backoff_factor=1, status_forcelist=[502, 503, 504])
  session.mount('https://', HTTPAdapter(max_retries=retries))
  try:
    check = session.get(f"https://catalog.roblox.com/v1/search/items/details?Category=3&CreatorTargetId={id}&CreatorType=2&Limit=30").result()
    check = check.json()
  except RequestException as e:
    print(e)
    return 0

  def get_page(cursor=None):
      nonlocal check
      try:
        if cursor:
          url = f"https://catalog.roblox.com/v1/search/items/details?Category=3&CreatorTargetId={id}&CreatorType=2&Limit=30&cursor={cursor}"
        else:
          url = f"https://catalog.roblox.com/v1/search/items/details?Category=3&CreatorTargetId={id}&CreatorType=2&Limit=30"
        check = session.get(url).result().json()
      except RequestException as e:
        print(e)  
        return 0
      return check

  while True:
      if "data" in check:
          clothings += len(check['data'])
      if "nextPageCursor" not in check or not check['nextPageCursor']:
          break
      else:
          check = get_page(check['nextPageCursor'])
  return clothings

def robux(id):
  # Import Local Cookie Variable
  global roblox_cookie
  session = FuturesSession()
  retries = Retry(total=5, backoff_factor=1, status_forcelist=[502, 503, 504])
  session.mount('https://', HTTPAdapter(max_retries=retries))
  try:
      # Send the request asynchronously and return a Future object
      future = session.get(f'https://economy.roblox.com/v1/groups/{id}/currency', cookies=roblox_cookie, timeout=5)
  except RequestException as e:
    print(e)
    return 0
  try:
    response = future.result()
    data = json.loads(response.text)
    if "robux" in data:
      robux = data.get("robux", 0)
    else:
      robux = 0
  except RequestException as e:
    print(e)
    return 0
  return robux


def gamevisits(id):
  # Create a FuturesSession object
  session = FuturesSession()
  retries = Retry(total=5, backoff_factor=1, status_forcelist=[502, 503, 504])
  session.mount('https://', HTTPAdapter(max_retries=retries))

  # Make the API request asynchronously
  try:
    future = session.get(f'https://games.roblox.com/v2/groups/{id}/gamesV2?accessFilter=2&limit=100&sortOrder=Asc', timeout=5)
  except RequestException as e:
    print(e)
    return 0

  # Wait for the request to complete and load the response into a dictionary
  try:
    response = future.result()
    os = json.loads(response.text)
    if "data" in os:
      data = os["data"]
    else:
      data = 0
      
  except RequestException as e:
    print(e)
    return 0

  # If there are no games, return "None"
  if not data:
    return 0
  
  # Find the total number of visits for all games
  total_visits = 0
  for game in data:
    visits = game["placeVisits"]
    total_visits += visits
  return total_visits
  
def gamecount(id):
  session = FuturesSession()
  retries = Retry(total=5, backoff_factor=1, status_forcelist=[502, 503, 504])
  session.mount('https://', HTTPAdapter(max_retries=retries))
  try:
      # Send the request asynchronously and return a Future object
      future = session.get(f'https://games.roblox.com/v2/groups/{id}/gamesV2?accessFilter=2&limit=100&sortOrder=Asc', timeout=5)
  except RequestException as e:
    print(e)
    return 0
  try:
    response = future.result()
    os = json.loads(response.text)
    if "data" in os:
      data = os["data"]
    else:
      data = 0
  except RequestException as e:
    print(e)
    return 0
  if not data:
    return 0
  else:
    return len(data)  

def groupimage(id):
  # Create a session with retries enabled
  session = FuturesSession()
  retry = Retry(connect=3, backoff_factor=0.5, status_forcelist=[502, 503, 504])
  adapter = HTTPAdapter(max_retries=retry)
  session.mount('https://', adapter)

  # Send the request asynchronously and return a Future object
  future = session.get(f'https://thumbnails.roblox.com/v1/groups/icons?groupIds={id}&size=150x150&format=Png&isCircular=false', timeout=5)

  # Wait for the request to complete and handle any errors that may occur
  try:
    response = future.result()
    icon_url = response.json()
    if "data" in icon_url and len(icon_url["data"]) > 0:
       image = icon_url["data"][0]["imageUrl"]
    else:
       image = "https://cdn.discordapp.com/emojis/894984341665488917.gif?size=44&quality=lossless"

  except RequestException as e:
    print(e)
    image = "https://cdn.discordapp.com/emojis/894984341665488917.gif?size=44&quality=lossless"
  return image 