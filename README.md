# CrawlingOP CURRENTLY NOT WORKING! 
Track your One Piece TGC Cards 🔍🏴‍☠️🃏🌊

The objective of this GitHub repository is to create an application that allows you to track your One Piece TGC Cards. To achieve this, I would like to develop a web application with user accounts where you can insert all the cards you want to track. The prices of individual cards or sets of four will be updated daily. Prices are obtained through [Cardmarket](https://www.cardmarket.com/en/OnePiece).

The project was initiated in November 2023 with the aim of leveraging the Cardmarket API to easily obtain public information without overloading the website. Unfortunately, after requesting access to the API and being denied, I had to explore alternative solutions to obtain the necessary data. The main challenge was that Cardmarket uses CloudFlare, making web scraping impossible (or nearly impossible).

After investigating various alternatives, I discovered that it was possible to access some websites via IP. I decided to give it a try, and fortunately, I found a suitable [IP address](http://85.215.9.83/es/OnePiece/Products/Singles/). I developed my project using this IP, but now it has been made private, requiring password access. It seems that they detected recurrent connections to it.

## How it was build? 

It's based on the [`pyspider`](https://docs.pyspider.org/en/latest/) library, and I've created a pipeline to deploy the spiders and create the necessary databases to process the data and obtain the following attributes from all the cards in the selected collections:
- Name
- Collection
- Number
- Rarity
- Price
- Playset_Price
- Date

To execute the program, you need to use the following code:
```bash
python deploy_spiders.py
```

However, since we're dealing with thousands of cards, using a single IP address will quickly result in access restrictions. Therefore, I implemented a system of rotating proxies to access the data. These proxies were periodically updated (and manually) through [free-proxy-list](https://free-proxy-list.net/), a website that provides a list of completely free proxies.

## 📝 TODO LIST
- Try other forms to Bypass Cloudflare security
- Try to obtain the API acces (again)
- Develop an application interface
