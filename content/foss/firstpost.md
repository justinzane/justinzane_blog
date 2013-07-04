Title: Restart with Pelican
Category: Python
Tags: pelican, publishing, blog, python, web

#Restarting with Pelican

##Restarting...

Over the years I've played around with a number of self-publishing tools, none of which really 
made me very happy. Some, like [Drupal](http://www.drupal.org/) were just total overkill for 
blogging, while others like simply posting to [Facebook](http://www.facebook.com/) or 
[Twitter](http://www.twitter.com/) were far from sufficiently expressive enough.

My favorite blogging tool has been [WordPress](http://www.wordpress.com/), and I still love it 
and recommend it as a great solution for most non-geeks. Wordpress is actively developed and 
supported by a non-evil corporate sponsor and has an absolutely *enormous* community of free and 
open source and commercial developers and users.

The vast WordPress universe means that there are plugins for almost any conceivable need and 
themes for any possible taste. It also ensures that the odds of experiencing a bug or questions
that has not already been answered is almost nil. The drawback that comes along with the benefits
of the large WordPress community is that it is a *big* target for 
[malicious hacks](http://www.cvedetails.com/vendor/2337/Wordpress.html).

The other serious drawback to WordPress and many other blog engines like it is that they are 
"Web 2.0" -- totally or mostly dynamically generating pages to serve each request. The problems 
with this are manifold: first, there is a large software stack required. Normally this includes

    - a web server like Apache or Nginx to serve static content and handle requests,

    - an application server to process the PHP/Ruby/Python code,

    - a database to hold the text/numeric data and

    - optional layers like an object cache, reverse proxies, etc.

All this requires significant skill and attention from the sysadmin. Keeping the whole stack 
updated to avoid security vulnerabilities while avoiding breaking dependencies can get tedious. 
While this is essential for any sort of major website, it is excessive for a blog.  

Second, having to run code in every layer of this stack for every request requires CPU cycles 
and server RAM that can be expensive on hosted or cloud platforms. Third, and peculiar to geeks 
like myself, is the level of distraction posed by the complexity of the server software and the 
endless variety of plugins, themes and other tweaks. I have spent hours with *mysqltuner*, 
*curl*, *httping*, etc. testing and tweaking the performance of a WordPress installation instead 
of actually publishing anything on it. 

##Static

One of the simplest and most effective ways to avoid the above mentioned problems with the 
dynamic web is to simple use static html -- the way the web was at its inception. Of course, 
while writing html by hand is rather easy, keeping a consistent look and feel across numerous 
pages is a total pain in the ass. 

One of the trends I noticed is the migration to *static blog engines*. Basically, this is the 
use of many of the same dynamic page generation tools to create complex and consistent static 
pages from: CSS/SASS/LESS/Javascript themes, Python/Ruby/PHP/etc. plugins and Jinja/Mako/Cheetah/etc.
templates. 

The key difference between this approach and the traditional *Web 2.0* model is that the pages
are only reenerated when the site gets new content, not on every request. This means that the 
dynamic generation code can reside anywhere -- like the author's laptop -- and only the static 
pages live on the server. That means that no attacks on the webserver can do any long term 
damage.

##Pelican

![pelican](static/images/pelican_clipart_01.jpg "Pelican")

> Pelican is a simple static blog generator. It parses markup files (Markdown or 
reStructuredText for now) and generates an HTML folder with all the files in it. I’ve chosen to 
use Python to implement Pelican because it seemed to be simple and to fit to my needs. ...

> ##Use case

> I was previously using WordPress, a solution you can host on a web server to manage your blog. 
Most of the time, I prefer using markup languages such as Markdown or reStructuredText to type 
my articles. To do so, I use vim. I think it is important to let the people choose the tool 
they want to write the articles. In my opinion, a blog manager should just allow you to take 
any kind of input and transform it to a weblog. That’s what Pelican does. You can write your 
articles using the tool you want, and the markup language you want, and then generate a 
static HTML weblog. 
[*Alexis Métaireau*, creator of Pelican](http://docs.getpelican.com/en/3.2/report.html)

Since I have a distinct preference for *algol-style* languages like Python and C, and a rather 
visceral distaste for PHP, Perl and the like; I was primarily interested in [Python based blog 
engines](http://wiki.python.org/moin/PythonBlogSoftware). As you can see from the python.org
list, there are a gazillion candidates, but; most of them are abandonware. 

Fortunately, a quick google for `"static blog engine"` led me to this excellent 
[article](http://siliconangle.com/blog/2012/03/20/5-minimalist-static-html-blog-generators-to-check-out/).
I am quite interested in node.js so [blacksmith](http://blog.nodejitsu.com/introducing-blacksmith) 
looked very interesting. Since one of my primary goals is to be able to start writing without 
messing around too much, I'm skiping this for now. 

Though Jekyll/Octopress seems like excellent choices, they are in Ruby and I have little desire
to learn Ruby at the moment. That left two choices, the traditional engines MovableType and 
WordPress in static mode or Pelican. Since using the traditional engines with static output 
requires the same complex stack using them dynamically, I went for Pelican. 

We will see how my choice fares as I publish this article...