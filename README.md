# 密码学第一次实验

## 第一题 Dan Boneh 第一周编程作业

### 题目说明
给与总共十一组由同一密钥加密的密文数据，求密钥与第八组密码，因为当流密码的一次性密钥被使用多次时就不再具有语义安全性，可以结合多个密文破解出明文
### 解题思路
空格space的ASCII码为0010 0000，大写字母A～Z的ASCII码为01000001～01011010，小写字母a～z的ASCII码为 01100001～01111010。因此可以**用space和字母做XOR操作，对字母进行大小写切换；而两个字母做XOR操作，结果将不在字母范围内**。

又由于将两个密文做XOR操作相当于将两个密文对应的明文做XOR操作，如果结果中某个位置出现字母，则说明这两个明文的其中一个在该位置可能为空格。故对11个密文两两做XOR操作，然后通过结果判断不同明文中可能存在空格的位置，然后将对应位置上的密文和space做XOR操作，就可得到对应位置的密钥信息，当获取到足够多的密钥信息后，即可对目标密文进行解密。
###结果
最后分析出：

密钥为66396e89c9dbd8cb9874352acd6395102eafce78aa7fed28a006bc98d29c5b69b0339a19f8aa401a9c6d708f80c066c763fef0123148cdd8e82d05ba98777335daefcecd59c433a6b268b60bf4ef03c9a61100bb09a3161edc704a3

第8组的明文为“ We can see the point where the chip is unhappy if a wrong bit is sent and consumes”
## 第二题 破解类维吉尼亚密码

### 题目说明
给出一段密文和加密程序，告知明文只包含大小写字母、标点符号和空格，没有数字和其他字符，要求给出密钥与明文。
### 解题思路
本质上是密钥重复使用问题，假设密钥长度为klen，则相隔n*klen的密文使用同一密钥进行加密。所以首先猜测密钥长度klen，再将密文分割成klen组，对每一组遍历密钥的所有可能取值，并与密文异或，找到并记录异或结果全为明文字符的可能密钥值。爆破密钥长度和可能密钥值
###结果
明文为：
Cryptography is the practice and study of techniques for, among other things, secure communication in the presence of attackers. Cryptography has been used for hundreds, if not thousands, of years, but traditional cryptosystems were designed and evaluated in a fairly ad hoc manner. For example, the Vigenere encryption scheme was thought to be secure for decades after it was invented, but we now know, and this exercise demonstrates, that it can be broken very easily.

## 第三题 Break repeating-key XOR

### 题目说明
这一题可以认为是上一题的加强。

- 猜测密钥长度后，将密文分成相应长度块，计算相邻块间的汉明距离，具有最小归一化汉明距离的块长度很可能是真实密钥长度。

- 用字母频率分析的方法爆破当前位置的密钥。

### 解题思路
基于汉明距离的统计特性：当用正确密钥长度对密文分组时，分组后的密文块因对应同一密钥加密，其汉明距离会显著小于随机分组。代码遍历可能的密钥长度（2~40），计算不同长度下分组密文的平均汉明距离并归一化（除以长度），取归一化值最小的长度作为最可能的密钥长度。恢复密钥确定密钥长度后，将密文按 “位置模密钥长度” 转置分块（例如密钥长度为 3 时，第 0、3、6… 字节组成块 1，第 1、4、7… 字节组成块 2，以此类推）。每个转置块实际是用同一密钥字节加密的单字节 XOR 密文，因此对每个块遍历 0~255 所有可能字节作为密钥，通过评估解密后文本的 “英文自然度”（可打印字符占比、空格和字母频率）筛选最优密钥字节，拼接得到完整密钥。解密明文用恢复的密钥对密文执行逐字节 XOR 操作（密钥循环复用），得到原始明文。
###结果
恢复的密钥: Terminator X: Bring the noise

解密后的明文:
I'm back and I'm ringin' the bell
A rockin' on the mike while the fly girls yell
In ecstasy in the back of me
Well that's my DJ Deshay cuttin' all them Z's
Hittin' hard and the girlies goin' crazy
Vanilla's on the mike, man I'm not lazy.

I'm lettin' my drug kick in
It controls my mouth and I begin
To just let it flow, let my concepts go
My posse's to the side yellin', Go Vanilla Go!

Smooth 'cause that's the way I will be
And if you don't give a damn, then
Why you starin' at me
So get off 'cause I control the stage
There's no dissin' allowed
I'm in my own phase
The girlies sa y they love me and that is ok
And I can dance better than any kid n' play

Stage 2 -- Yea the one ya' wanna listen to
It's off my head so let the beat play through
So I can funk it up and make it sound good
1-2-3 Yo -- Knock on some wood
For good luck, I like my rhymes atrocious
Supercalafragilisticexpialidocious
I'm an effect and that you can bet
I can take a fly girl and make her wet.

I'm like Samson -- Samson to Delilah
There's no denyin', You can try to hang
But you'll keep tryin' to get my style
Over and over, practice makes perfect
But not if you're a loafer.

You'll get nowhere, no place, no time, no girls
Soon -- Oh my God, homebody, you probably eat
Spaghetti with a spoon! Come on and say it!

VIP. Vanilla Ice yep, yep, I'm comin' hard like a rhino
Intoxicating so you stagger like a wino
So punks stop trying and girl stop cryin'
Vanilla Ice is sellin' and you people are buyin'
'Cause why the freaks are jockin' like Crazy Glue
Movin' and groovin' trying to sing along
All through the ghetto groovin' this here song
Now you're amazed by the VIP posse.

Steppin' so hard like a German Nazi
Startled by the bases hittin' ground
There's no trippin' on mine, I'm just gettin' down
Sparkamatic, I'm hangin' tight like a fanatic
You trapped me once and I thought that
You might have it
So step down and lend me your ear
'89 in my time! You, '90 is my year.

You're weakenin' fast, YO! and I can tell it
Your body's gettin' hot, so, so I can smell it
So don't be mad and don't be sad
'Cause the lyrics belong to ICE, You can call me Dad
You're pitchin' a fit, so step back and endure
Let the witch doctor, Ice, do the dance to cure
So come up close and don't be square
You wanna battle me -- Anytime, anywhere

You thought that I was weak, Boy, you're dead wrong
So come on, everybody and sing this song

Say -- Play that funky music Say, go white boy, go white boy go
play that funky music Go white boy, go white boy, go
Lay down and boogie and play that funky music till you die.

Play that funky music Come on, Come on, let me hear
Play that funky music white boy you say it, say it
Play that funky music A little louder now
Play that funky music, white boy Come on, Come on, Come on
Play that funky music

## 第四题 Cracking SHA1-Hashed Passwords

### 题目说明
给出用户输入密码所使用的按键，密码的长度和密码SHA1之后的值。
### 解题思路
密码一般在5到9位左右甚至更高，对所有可能的情况进行尝试，结果SHA-1之后的值与所给值进行比较，直至尝试出正确的密码
###结果

password为(Q=win*5
