# HorribleSubs Hourly Notifier
[![CircleCI](https://circleci.com/gh/Fawers/horriblesubs-hourly-notifier.svg?style=svg)](https://circleci.com/gh/Fawers/horriblesubs-hourly-notifier)

First things first: [here](https://t.me/horriblesubs_hourly_releases) is the Telegram channel.
Tune in for the latest updates.

***

| TOC |
|:---:|
| Inspiration |
| Idea |
| Contributing |
| Running |
| Tests |
| Misc |

***

## Inspiration
I used to have a Crunchyroll subscription until not too long ago. Being an anime consumer since
2009, it really fit my needs: online streaming, no need to download, several subtitle language
options...  
That is, until I realized the service was getting worse, and I couldn't even enjoy all the shows.

Crunchyroll had a buggy player with buffering problems (don't know whether they fixed it up
since my last receipt dates to December 2017), and many shows aren't available simply because of
region limitations (this seems to continue). Now compare this vs. fansubs that make all titles on
Crunchyroll + many others available for free and with a much higher quality, and here we are.

At first I stuck with Brazilian fansubs for the linguistical comfort, but these often take too
long to release the shows, or release it quickly but filled with writing mistakes - grammar,
context, mispellings...

And that led me to [HorribleSubs](https://horriblesubs.info), a fansub with quick releases and
good writing. I'm fluent in English, so the subs being all in English is no problem at all.
Knowing that they also provide RSS feeds, and being a
[Telegram](https://telegram.org) bot developer, I thought, "why not make it notify me instead of
checking time after time to see what's out?," which leads us to the

## Idea
Technically, there still is someone (or something) checking their site time after time to see
what is out. But the point is, this _something_ comes to us and share this info with us, so we
can just sit back and wait for our favorite shows to be released. There are no direct links to
downloads on the Telegram channel, so the user still has to access their website and manually
download the `.torrent` files or consume the magnet links (and I made it this way on purpose).

The execution is rather simple: consume the
[RSS feed](http://www.horriblesubs.info/rss.php?res=720), identify what has already been
shared by checking each show _guid_, gather everything in one single message, and send it to the channel.  
As to _how_ it is done... well, you **are** in the repository page. Go take a look at the code.

## Contributing
Like the idea and want to share some knowledge? You're more than welcome to do so!  
Just follow the standard guidelines and you're good to go:
fork, checkout to new branch, code, test, (or test, and then code), PR.

## Running
Two environment variables are needed in order to run [self](#): `TGBOT` and `TGCHANNEL`, where:

* `TGBOT` is the Telegram bot token;
* `TGCHANNEL` is the Telegram public channel `@username`.

## Tests
```sh
pip install -r requirements-tests.txt
python -m pytest
```

***

## Misc
Code quality: `flake8`  
Unit testing: `pytest`  
CI/CD: `circle-ci`
