# PyMangler

###
A wordlist mangler that has the ability to analyze existing lists and generate large quantities of passwords based on patterns found therein.  A fairly methodical approach to password cracking, to be used after traditional methods have failed.

<br>

##
How it works

<ol>
	<li>Analyzes wordlist to determine patterns such as:</li>
	<ul>
		<li>common simple masks (word-digit, word-special, etc.)</li>
		<li>common numbers and special characters</li>
		<li>commonly used words (e.g. P@ssw0rd)</li>
	</ul>
	<li>Calculates total keyspace</li>
	<li>Generates passwords based on learned patterns</li>
	<li>Given target crack time, adjusts accordingly by trimming less common attributes</li>
</ol>




<br>

#### Basic usage:
~~~~
# mutate each entry in wordlist with leet characters
# common numbers & special characters are appended / prepended
<strong>cat wordlist | ./pymangler.py --leet</strong>
~~~~

<br>

#### Advanced usage:
~~~~
# analyze wordlist and save statistics into file
<strong>cat rockyou.txt | ./liststat.py -s rockyou_stats</strong>

# generate passwords based on the string 'evilcorp' for 36 hours
# progresses from simple to complex
<strong>echo 'evilcorp' | ./pymangler -l rockyou_stats --time 36</strong>
~~~~