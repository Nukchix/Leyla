import re
from datetime import datetime
import typing
import os
import random
import json

import aiohttp
import disnake
from disnake.ext import commands
from Tools.links import fotmat_links_for_avatar, emoji_converter, emoji_formats
from Tools.decoders import Decoder
from Tools.exceptions import CustomError
import emoji as emj
from bs4 import BeautifulSoup
from Tools.buttons import CurrencyButton


class Utilities(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command(
        description="Вывод аватара участника"
    )
    async def avatar(self, inter, user: disnake.User = commands.Param(lambda inter: inter.author)):
        embed = await self.bot.embeds.simple(
            title=f"Аватар {'бота' if user.bot else 'пользователя'} {user.name}",
            image=user.display_avatar.url
        )
        return await inter.send(embed=embed)

    @commands.slash_command(
        description='Перевод в/из азбуки морзе.'
    )
    async def morse(self, inter, variant: typing.Literal['to', 'from'], *, code):
        if variant == 'to':
            morse = Decoder().to_morse(code)
        elif variant == 'from':
            morse = Decoder().from_morse(code)

        embed = await self.bot.embeds.simple(
            title='Decoder/Encoder морзе.',
            description=morse
        )
        await inter.send(embed=embed)

    @commands.slash_command(
        description="Вывод информации о гильдии",
    )
    async def guild(self, inter: disnake.ApplicationCommandInteraction):
        information = (
            f'Участников: **{len(inter.guild.members)}**',
            f'Эмодзи: **{len(inter.guild.emojis)}**',
            f'Количество ролей: **{len(inter.guild.roles)}**',
            f'Ботов на сервере: **{len(list(filter(lambda user: user.bot, inter.guild.members)))}**'
        )
        embed = await self.bot.embeds.simple(
            title=f'Информация о гильдии {inter.guild.name}',
            description="\n".join(information)
        )

        if inter.guild.banner:
            embed.set_thumbnail(inter.guild.banner.url)

        if inter.guild.icon:
            embed.set_thumbnail(inter.guild.icon)

        await inter.send(embed=embed)

    @commands.slash_command(
        description="Вывод информации о юзере"
    )
    async def user(self, inter, user: disnake.User = commands.Param(lambda inter: inter.author)):
        embed = await self.bot.embeds.simple(title=f'Информация о {"боте" if user.bot else "пользователе"} {user.name}')

        if user.banner:
            embed.set_image(url=user.banner.url)

        embed.set_image(url=user.display_avatar.url)
        embed.set_footer(text=f"ID: {user.id}")
        
        main_information = [
            f"Зарегистрировался: **<t:{round(user.created_at.timestamp())}:R>**",
            f"Полный никнейм: **{str(user)}**",
        ]

        if user in inter.guild.members:
            user_to_member = inter.guild.get_member(user.id)
            second_information = [
                f"Зашёл(-ла) на сервер: **<t:{round(user_to_member.joined_at.timestamp())}:R> | {(datetime.utcnow() - user.created_at.replace(tzinfo=None)).days} дней**",
                f"Количество ролей: **{len(list(filter(lambda role: role, user_to_member.roles)))}**",
            ]

        embed.description = "\n".join(main_information) + "\n" + "\n".join(second_information) if user in inter.guild.members else "\n".join(main_information)

        await inter.send(embed=embed)

    @commands.slash_command(
        description="Получить эмодзик"
    )
    async def emoji(self, inter, emoji):
        if emoji in emj.UNICODE_EMOJI_ALIAS_ENGLISH:
            await inter.send(emoji)
        else:
            get_emoji_id = int(''.join(re.findall(r'[0-9]', emoji)))
            url = f"https://cdn.discordapp.com/emojis/{get_emoji_id}.gif?size=480&quality=lossless"
            embed = await self.bot.embeds.simple(
                title=f"Эмодзи **{emoji}**",
                image=await emoji_converter('webp', url)
            )

            await inter.send(embed=embed)

    @commands.slash_command(description="Данная команда может поднять сервер в топе на boticord'e")
    async def up(self, inter: disnake.ApplicationCommandInteraction):
        data = {
            "serverID": str(inter.guild.id),
            "up": 1,
            "status": 1,
            "serverName": inter.guild.name,
            "serverAvatar": inter.guild.icon.url if inter.guild.icon else None,
            "serverMembersAllCount": len(inter.guild.members),
            "serverOwnerID": str(inter.guild.owner_id),
        }

        async with self.bot.session.post(
            'https://api.boticord.top/v1/server', 
            headers={'Authorization': os.environ['BCORD']}, 
            json=data
        ) as response:
            x = await response.json()
        
            if not response.ok:
                return
            else:
                server = data["serverID"]
                embed = await self.bot.embeds.simple(
                    title='BotiCord',
                    description="У меня нет доступа к API методу(\nЗайдите на [сервер поддержки](https://discord.gg/43zapTjgvm) для дальнейшей помощи" if "error" in x else x["message"], 
                    url=f"https://boticord.top/add/server" if "error" in x else f"https://boticord.top/server/{server}"
                )

                await inter.send(embed=embed)

    @commands.slash_command(name='emoji-random', description="Я найду тебе рандомный эмодзик :3")
    async def random_emoji(self, inter):
        emoji = random.choice(self.bot.emojis)
        await inter.send(embed=await self.bot.embeds.simple(description="Эмодзяяяяяяяя", image=emoji.url, fields=[{'name': 'Скачать эмодзик', 'value': f'[ТЫКТЫКТЫК]({emoji.url})'}]))

    @commands.slash_command(name="random-anime", description="Вы же любите аниме? Я да, а вот тут я могу порекомендовать вам аниме!")
    async def random_anime(self, inter):
        url = 'https://animego.org'

        async with aiohttp.ClientSession(
            headers={
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36 OPR/80.0.4170.91',
                'cookie': os.environ['COOKIE']
            }) as session:
            async with session.get(f'{url}/anime/random') as res:
                soup = BeautifulSoup(await res.text(), 'html.parser')
                name = soup.select('.anime-title')[0].find('h1', class_=False).text
                img = soup.find('div', class_='anime-poster').find('img', class_=False).get('src')
                desc = soup.find('div', class_='description').text
                url = f'{url}{res.url._val.path}'
                await session.close()
        desc = re.sub('\n', '', desc, 1)
        await inter.send(embed=await self.bot.embeds.simple(
                description=f'**[{name}]({url})**\n**Описание**\n> {desc}',
                thumbnail=re.sub('media/cache/thumbs_\d{3}x\d{3}', '', img)
            )
        )

    @commands.slash_command(name="currency", description="Подскажу вам курс той или иной валюты :) (В рублях!)")
    async def currency_converter(self, inter, currency, how_many: int = 0):
        async with self.bot.session.get('https://www.cbr-xml-daily.ru/daily_json.js') as response:
            cb_data = await response.text()

        json_cb_data = json.loads(cb_data)
        get_currency = {i:j['Name'] for i, j in json_cb_data['Valute'].items()}
        data = json_cb_data["Valute"]

        if currency.upper() in data:
            upper_currency = currency.upper()

            await inter.send(
                embed=await self.bot.embeds.simple(
                    title=f'Курс - {get_currency[upper_currency]} ({upper_currency})',
                    description=f'{get_currency[upper_currency]} на данный момент стоит **{round(data[upper_currency]["Value"])}** рублей. ({round(data[upper_currency]["Value"] - data[upper_currency]["Previous"], 1)})',
                    fields=[
                        {
                            "name": "Абсолютная погрешность", 
                            "value": abs(data[upper_currency]["Value"] - round(data[upper_currency]["Value"])), 
                            'inline': True
                        }, 
                        {
                            "name": "Прошлая стоимость", 
                            "value": data[upper_currency]['Previous'], 
                            'inline': True
                        }, None if how_many == 0 else {
                            "name": f"Сколько (**{how_many} {upper_currency}**) в рублях", 
                            "value": how_many * round(int(data[upper_currency]['Value']), 2),
                        }
                    ],
                    footer={"text": 'Вся информация взята с оффициального API ЦБ РФ.', 'icon_url': 'https://cdn.discordapp.com/attachments/894108349367484446/951452412714045460/unknown.png?width=493&height=491'}
                ), view=CurrencyButton()
            )
        else:
            await inter.send(embed=await self.bot.embeds.simple(title='Курс... Так, стоп', description="Такой валюты не существует!!"))

def setup(bot: commands.Bot):
    bot.add_cog(Utilities(bot))
