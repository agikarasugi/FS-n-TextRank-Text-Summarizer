from textrank import TextRank
from article import get_text

text = get_text('https://www.bbc.com/news/world-us-canada-47848619')
tr = TextRank(text, lang='english', metric='log', graph='HITS')
tr.summarize()


'''
Shunichi Suzuki, who had been Olympics minister before Mr Sakurada was appointed last October, will return to the post.
In February Mr Sakurada had to make another apology, after arriving three minutes late to a parliamentary meeting.
"I deeply apologise for his remark to the people in the disaster-hit areas," said Mr Abe.
It is not the first time Mr Sakurada has been forced to apologise.
After accepting Mr Sakurada's resignation, Prime Minister Shinzo Abe apologised for appointing him.
Image copyright AFP  Japan's Olympics Minister Yoshitaka Sakurada has resigned over comments that offended people affected by a huge tsunami and earthquake in 2011.
Mr Sakurada also admitted last year to never having used a computer, despite being Japan's cyber security minister.

Shunichi Suzuki, who had been Olympics minister before Mr Sakurada was appointed last October, will return to the post.
"I deeply apologise for his remark to the people in the disaster-hit areas," said Mr Abe.
It is not the first time Mr Sakurada has been forced to apologise.
After accepting Mr Sakurada's resignation, Prime Minister Shinzo Abe apologised for appointing him.
Image copyright AFP  Japan's Olympics Minister Yoshitaka Sakurada has resigned over comments that offended people affected by a huge tsunami and earthquake in 2011.
The 2011 tsunami left more than 20,000 dead and caused a meltdown at the Fukushima Daiichi nuclear plant.
Mr Sakurada also admitted last year to never having used a computer, despite being Japan's cyber security minister.

'''