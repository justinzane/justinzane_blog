Title: Bicycles and [Lack of] Benchmarks
Category: cycling
Tags: cycling, value, parts, benchmarks
Summary: Thoughts on empirical measurement of bike parts.

# Bicycles and [Lack of] Benchmarks

In the world of computer parts, there are innumerable benchmarks for almost all purposes. 
Disks and other storage -- dbench, CPUs -- SPEC Int, FP, etc., GPUs -- almost every game 
has a scripted benchmark mode, and there are tons of GPGPU benchmarks as well. Same goes 
for RAM, cooling fans, network adapters, power supplies and so on.

That gives the buyer the ability to determine an objective performance per dollar figure for 
the purpose that he or she intends. As an example, when replacing the CPU, RAM and motherboard 
in our family media PC, I know that the minimum requirements were 8GB RAM, 2 PCIe slots, 4 SATA 
ports. Beyond that, the biggest factor was low power dissipation. From there I could easily 
lookup benchmarks of likely Intel and AMD CPUs and plug them into a spreadsheet along with 
their NewEgg prices. The best pick simply had the the best number in the final column. Simple.

Since there is almost no human factor and an amazingly easy way to measure part performance, 
computer kit is far, far different from cycle kit. With bikes, getting a consistent, easily 
repeatable test circumstance is **very** challenging. Even the same person, riding the same 
route will experience different circumstances for every ride if they are not riding in a closed 
velodrome. Different winds, temperatures, traffic, nutrition, chicken playing ground squirrels, 
and so on make for slight differences between rides that limit the ability to do good benchmarks. 

That said, though, excepting aesthetics and conspicuous consumption; every part on a cycle has 
a measurable impact on the conversion of muscular exertion by the rider to forward motion. Even 
thing that are not considered performance parts, say pannier racks, have a measurable 
performance. In the case of a rack, performance metrics might be weight, drag coefficient and 
MTBF (mean time between failure) with a standard test bag and load. 

For a long distance touring rider, weight and drag might be quite important. For the Dutch 
homemaker simply concerned with getting to the butcher's and baker's and back, MTBF (mean time 
between failures), a measure of reliability and durability, is likely to be of greater 
importance than a few dozen grams. And, since he or she will often be riding with semi-fragile 
items like a dozen eggs, speed -- and its associated exponential drag -- is going to be kept 
minimal anyway. That means that there is a way to develop a qualitative value for potential 
racks.

<?xml version="1.0" encoding="UTF-8"?>
<math xmlns="http://www.w3.org/1998/Math/MathML" display="block">
 <semantics>
  <mtable>
   <mtr>
    <mtd>
     <mrow>
      <msub>
       <mi mathvariant="italic">score</mi>
       <mi mathvariant="italic">mass</mi>
      </msub>
      <mrow>
       <mspace width="2em"/>
       <mo stretchy="false">=</mo>
       <mspace width="2em"/>
      </mrow>
      <mrow>
       <msub>
        <mi mathvariant="italic">weight</mi>
        <mi mathvariant="italic">mass</mi>
       </msub>
       <mo stretchy="false">×</mo>
       <mfrac>
        <mrow>
         <msub>
          <mi mathvariant="italic">mass</mi>
          <mi mathvariant="italic">max</mi>
         </msub>
         <mo stretchy="false">−</mo>
         <msub>
          <mi mathvariant="italic">mass</mi>
          <mi mathvariant="italic">part</mi>
         </msub>
        </mrow>
        <mrow>
         <msub>
          <mi mathvariant="italic">mass</mi>
          <mi mathvariant="italic">max</mi>
         </msub>
         <mo stretchy="false">−</mo>
         <msub>
          <mi mathvariant="italic">mass</mi>
          <mi mathvariant="italic">min</mi>
         </msub>
        </mrow>
       </mfrac>
      </mrow>
     </mrow>
    </mtd>
   </mtr>
   <mtr>
    <mtd>
     <mrow>
      <msub>
       <mi mathvariant="italic">score</mi>
       <mi mathvariant="italic">drag</mi>
      </msub>
      <mrow>
       <mspace width="2em"/>
       <mo stretchy="false">=</mo>
       <mspace width="2em"/>
      </mrow>
      <mrow>
       <msub>
        <mi mathvariant="italic">weight</mi>
        <mi mathvariant="italic">drag</mi>
       </msub>
       <mo stretchy="false">×</mo>
       <msubsup>
        <mi mathvariant="italic">speed</mi>
        <mi mathvariant="italic">flat</mi>
        <mn>2</mn>
       </msubsup>
       <mo stretchy="false">×</mo>
       <mfrac>
        <mrow>
         <msub>
          <mi mathvariant="italic">drag</mi>
          <mi mathvariant="italic">max</mi>
         </msub>
         <mo stretchy="false">−</mo>
         <msub>
          <mi mathvariant="italic">drag</mi>
          <mi mathvariant="italic">part</mi>
         </msub>
        </mrow>
        <mrow>
         <msub>
          <mi mathvariant="italic">drag</mi>
          <mi mathvariant="italic">max</mi>
         </msub>
         <mo stretchy="false">−</mo>
         <msub>
          <mi mathvariant="italic">drag</mi>
          <mi mathvariant="italic">min</mi>
         </msub>
        </mrow>
       </mfrac>
      </mrow>
     </mrow>
    </mtd>
   </mtr>
   <mtr>
    <mtd>
     <mrow>
      <msub>
       <mi mathvariant="italic">score</mi>
       <mi mathvariant="italic">mtbf</mi>
      </msub>
      <mrow>
       <mspace width="2em"/>
       <mo stretchy="false">=</mo>
       <mspace width="2em"/>
      </mrow>
      <mrow>
       <msub>
        <mi mathvariant="italic">weight</mi>
        <mi mathvariant="italic">mtbf</mi>
       </msub>
       <mo stretchy="false">×</mo>
       <mfrac>
        <mrow>
         <msub>
          <mi mathvariant="italic">mtbf</mi>
          <mi mathvariant="italic">part</mi>
         </msub>
         <mo stretchy="false">−</mo>
         <msub>
          <mi mathvariant="italic">mtbf</mi>
          <mi mathvariant="italic">min</mi>
         </msub>
        </mrow>
        <mrow>
         <msub>
          <mi mathvariant="italic">mtbf</mi>
          <mi mathvariant="italic">max</mi>
         </msub>
         <mo stretchy="false">−</mo>
         <msub>
          <mi mathvariant="italic">mtbf</mi>
          <mi mathvariant="italic">min</mi>
         </msub>
        </mrow>
       </mfrac>
      </mrow>
     </mrow>
    </mtd>
   </mtr>
   <mtr>
    <mtd>
     <mrow/>
    </mtd>
   </mtr>
   <mtr>
    <mtd>
     <mrow>
      <mi mathvariant="italic">value</mi>
      <mrow>
       <mspace width="2em"/>
       <mo stretchy="false">=</mo>
       <mspace width="2em"/>
      </mrow>
      <mfrac>
       <mrow>
        <msub>
         <mi mathvariant="italic">score</mi>
         <mi mathvariant="italic">mass</mi>
        </msub>
        <mo stretchy="false">+</mo>
        <msub>
         <mi mathvariant="italic">score</mi>
         <mi mathvariant="italic">drag</mi>
        </msub>
        <mo stretchy="false">+</mo>
        <msub>
         <mi mathvariant="italic">score</mi>
         <mi mathvariant="italic">mtbf</mi>
        </msub>
       </mrow>
       <msub>
        <mi mathvariant="italic">cost</mi>
        <mi mathvariant="italic">part</mi>
       </msub>
      </mfrac>
     </mrow>
    </mtd>
   </mtr>
  </mtable>
  <annotation encoding="StarMath 5.0">score_mass ~=~ 
        weight_mass times {{mass_max - mass_part} over {mass_max - mass_min}}
newline
score_drag ~=~ 
        weight_drag times speed_flat^2 times {{ drag_max - drag_part} over {drag_max - drag_min}}
newline
score_mtbf ~=~ 
        weight_mtbf times {{mtbf_part - mtbf_min} over {mtbf_max - mtbf_min}}
newline
newline
value ~=~ { score_mass + score_drag + score_mtbf } over { cost_part }
newline
</annotation>
 </semantics>
</math>

Now, doing comprehensive testing for racks is a *tad* over-the-top. The wind tunnel rental costs 
alone are insane. The core logic, though is the same for basically all components that go onto 
a cycle frame as well as the frame itself.

##Profusion of Pretentious Products

From what I've read, for the vast majority of cycling history, component makers made one or 
possibly two lines of parts. Recently, however, there has been a tremendous consolidation of the 
bicycle component industry with a few manufactures like Shimano, Campagnolo and SRAM thoroughly 
dominating the market.

And, these companies like those in most consumer businesses have created a plethora of product 
lines at widely variant price points. Just consider [Shimano]("http://productinfo.shimano.com/lineupchart.html"). Their road line as of this writing 
(2014-08-22) and based on Shimano's site and [Harris Cyclery](http://http://harriscyclery.net/) is:

| Line Name       | Line | Shifter Set | Price (USD) |
| --------------- | ---- | ----------- | ----------- |
| *Dura-Ace*      | 9000 | ST-9001 | 540.95 |
| *Dura-Ace 9070* | 9070 | ST-9070 | 700.95 |
| *Ultegra*       | 6800 | ST-6800 | 330.95 |
| *Ultegra 6870*  | 6870 | ST-6870 | 370.95 |
| *105*           | 5800 | ST-5800 | 290.95 |
| *Tiagra*        | 4600 | ST-4600 | 271.95 |
| *Sora*          | 3500 | ST-3500 | 218.95 |
| *Claris*        | 2400 | ST-2400 | 134.99 |
| *Tourney*       | A070 | ST-A070 | 103.95 |
| OEM             | A050 | ST-A050 | NA     |

![Shimano Road Shifter Chart](/images/2014-08-23_shimano_graph.svg)

Add to that their mountain line and utility/commuter/whatever lines and there are literally 
dozens of choices of Shimano parts that all perform the same basic function. Campagnolo is 
almost as bad with: *Super Record EPS*, *Record EPS*, *Athena EPS*, *Super Record*, *Record*, 
*Chorus*, *Athena*, *Centaur*, and *Veloce*. 

Since bicycle components, with the minor exception of shift-by-wire parts like the 9070/6870 
lines from Shimano and the EPS lines from Campy, are **simple gears, pulleys and levers**; 
this is obviously a case of MBAs and marketers gone wild. No engineer without multiple 
personality disorder would do anything like that.

And, from a value perspective, it is hard to understand the progression. In what contexts is 
the ST-9001 *Dura-Ace* brifter (integrated brake and shift levers) set 520% better than the 
ST-A070 *Tourney* set? Is the same pro rider 5.2 times more likely to win a stage in the *Tour 
de France* with the DAs? Will a fat old guy like me lose weight 5.2 times faster riding with 
the DAs? Enjoy the ride 5.2 times more? Will the DAs have 5.2 time the resale value in ten 
years? 

In short, what data justifies the 5.2 times larger hole in one's wallet when purchasing the top 
of the line Shimano brifters? When building a computer for hosting a PostGIS geographical 
database to be used for a navigation server, I can justify pretty exactly the value of a CPU 
that is 520% the price of an entry level Intel Celeron. How does one do the same for their bike?

##Why Empirical Benchmarks Matter

For some buyers, performance does not really matter; they care more about perceptions and the 
prestige that they believe high end components bring them. For these people, and for [weight 
weeines](http://www.urbandictionary.com/define.php?term=weight%20weenie) actual price to 
performance is irrelevant since they have emotionally based, not rational purchasing strategies. 

Another group that cares little about value is the sponsored professional, since they get paid 
to ride their gear. The inverse tends apply to penny pinchers like myself. For some cyclists, a 
very tightly circumscribed budget means that they can only consider the lowest cost parts, so 
the question of whether *Dura-Ace* shifts smoother than *Super Record* is as relevant as whether 
the seats on the Space Shuttle were more confortable than those on Soyuz.

Even for those folks like me with limited resources, though, having good empirical data about 
components would make a world of difference. Consider the following set of weights -- weights 
in the statistical sense, not the gravitational one:

| Factor       | Weight |
| ----------   | -.---- |
| Fit          | 0.40 |
| Functionality| 0.40 |
| Durability   | 0.05 |
| Ease Inst.   | 0.05 |
| Appearance   | 0.05 |
| Brand        | 0.00 |
| Mass         | 0.00 |
| Drag         | 0.05 |

I'm very tall 6'3" -- 190.5cm -- and about forty pounds -- 88000.0 grams -- overweight. That 
means I care a lot about how well saddles, seat post angles, top tube length, bar dimensions and 
so on make me confortable on my bike. It also means that I could give a rodent's posterior about 
the fact that a fibre-reinforced plastic shift lever weights 8.2 grams less than an aluminum 
one. I can save far more weight by actually riding than by anything that advanced materials 
save. 

For someone I know who is average height, very fit and trim, financially secure, but not a
competetive rider, the value of component mass might be more like 5% or 10% while fit tends to 
be more of a sure bet. For some people, like my wife who lives with the legacy of some old 
injuries and arthritis, the fit weight goes up to highest position making up maybe 80% of the 
choice.

For all of us, however, choosing components is currently a matter of guesswork. While some 
fortunate riders live near a quality local bike shop with generous test ride policies; many of 
us do not. My LBS, for example, needed major cajoling to let my wife test ride an $800.00 bike 
up and down the flat, paved dead-end road in front of the shop. They seem thoroughly unwilling 
to do something like let one pop a saddle on their bike for a test ride. That means that for us, 
the **only** way to try different components is to buy them and pay the return freight for ones 
we do not like.

Since practical experience is out of the question, reviews on bike forums and online stores are 
the only data available. And, almost by definition, that data is nothing more than a non-random 
sampling of subjective opinion. Considering the fact that it is psychologically very difficult 
for people to criticize their own decisions, people who are willing to say that the several 
thousand that they spend on a *Super Record* or *Dura-Ace* groupset did not give them 
significantly more value than their old *Veloce* or *Sora* bits.

##What I Want

Had I a magic wand, I'd make a wind tunnel, dyanamometer, robot legs, robot hands, and various 
and sundry sensors appear in my yard. Then, after convincing Shimano, SRAM, Campagnolo, 
Microshift, Weinmann, Alex, Zipp, Jagwire, Sella Italia, Brooks, ... to send me samples of their 
kit, I could make this happen myself.

In reality, I would like to start by hearing what attempts have been made already in this regard 
and whether anyone else finds this to be a good idea.
