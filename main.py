import scrapy
import argparse

class LoLScrap(scrapy.Spider):
  name = 'lolscrap'
  start_urls = []

  def __init__(self, patch):
    elos = ["iron", "bronze", "silver", "gold", "platinum", "emerald", "diamond", "master", "grandmaster", "challenger"]
    regions = ["br", "na", "jp", "euw", "eune", "las", "kr", "tw", "lan", "sg", "ph", "vn", "oce"]
    self.patch = patch
    for region in regions:
      for elo in elos:
        self.start_urls.append("https://www.metasrc.com/lol/" + region + "/" +
                          self.patch + "/stats?ranks=" + elo)

  def parse(self, response):
      for url in self.start_urls:
        yield response.follow(url, self.parser_general_info)

  def parser_specific_info(self, response):
      info = response.request.meta['general_info']

      games = response.css("#splash-content > div._fcip6v._eq293a._r14nwh > span > div > span:nth-child(6) > span::text").get()
      rolerate = response.css("#splash-content > div._fcip6v._eq293a._r14nwh > span > div > span:nth-child(3) > span::text").get()
      winrate = response.css("#splash-content > div._fcip6v._eq293a._r14nwh > span > div > span:nth-child(2) > span::text").get()
      banrate = response.css("#splash-content > div._fcip6v._eq293a._r14nwh > span > div > span:nth-child(5) > span::text").get()
      tier = response.css("#splash-content > div._fcip6v._eq293a._r14nwh > span > div > span:nth-child(1) > span::text").get()
      kda = response.css("#splash-content > div._fcip6v._eq293a._r14nwh > span > div > span:nth-child(7) > span::text").get()
      pickrate = response.css("#splash-content > div._fcip6v._eq293a._r14nwh > span > div > span:nth-child(4) > span::text").get()

      info['games'] = int(games)
      info['pickrate'] = float(pickrate.replace("%","")) / 100
      info['rolerate'] = float(rolerate.replace("%","")) / 100
      info['winrate'] = float(winrate.replace("%","")) / 100
      info['banrate'] = float(banrate.replace("%","")) / 100
      info['tier'] = tier
      info['kda'] = float(kda)


      yield info

  def parser_general_info(self, response):
    elo = response.url.split("?ranks=")[1]
    patch = response.css("#splash-content > div:nth-child(1) > h1 > span._gct17l::text").get()
    region = response.request.url.split('/')[4]

    for champions in response.css("tbody > tr"):
      champ = {
        'name': champions.css("td:nth-child(1) > span::text").get(),
        'image_url': champions.css("td:nth-child(1) > a > img::attr(data-src)").get(),
        'role': champions.css("td:nth-child(2) > div::text").get(),
        'trend': champions.css("td:nth-child(5)::text").get(),
        'elo' : elo,
        'patch' : patch.split()[1],
        'region' : region,
        'score': float(champions.css("td:nth-child(4)::text").get())
      }
      link = champions.css("td:nth-child(1) > a::attr(href)").get()
    
      yield scrapy.Request(url=link, dont_filter=True, callback=self.parser_specific_info, meta={'general_info':champ})

    