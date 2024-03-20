import discord
from discord.ext import commands
from korcen import korcen
import json


class Bot(commands.Bot):
    def __init__(self, **kwargs):
        super().__init__(command_prefix=["/"], intents=discord.Intents.all(), case_insensitive=True, sync_command=True, help_command=None)

    async def on_ready(self):
        print(f"Logged in as {self.user}")
        await self.change_presence(status=discord.Status.online)
        await bot.change_presence(activity=discord.CustomActivity(name=f'{len(self.guilds)}개의 서버에서 일하는 ing..', type=5))
        await self.tree.sync()


intents = discord.Intents.all()
bot = Bot(intents=intents)


def open_log_channel():
    try:
        with open("log_channel.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def save_log_channel(channel):
    with open("log_channel.json", "w") as f:
        json.dump(channel, f, indent=4)


def open_warn():
    try:
        with open("warn.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def save_warn(warns):
    with open("warn.json", "w") as f:
        json.dump(warns, f, indent=4)


def open_swear():
    try:
        with open("swear.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def save_swear(swear):
    with open("swear.json", "w") as f:
        json.dump(swear, f, indent=4)


def open_hello_log():
    try:
        with open("hello_log.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def save_hello_log(hello_log):
    with open("hello_log.json", "w") as f:
        json.dump(hello_log, f, indent=4)


def open_notice():
    try:
        with open("notice.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def save_notice(notice):
    with open("notice.json", "w") as f:
        json.dump(notice, f, indent=4)


def check_admin(ctx):
    if ctx.author.guild_permissions.administrator:
        return True
    else:
        return False



class MyModal(discord.ui.Modal, title="가르치기"):
    m_title = discord.ui.TextInput(
        style=discord.TextStyle.short,
        label="공지 제목",
        required=False,
        placeholder="공지 제목은 여기에!"
    )

    m_description = discord.ui.TextInput(
        style=discord.TextStyle.long,
        label="공지 내용",
        required=False,
        placeholder="공지 내용은 요가에!"
    )

    async def on_submit(self, interaction: discord.Interaction):
        keyword = self.m_title.value
        description = self.m_description.value
        notice = open_notice()
        if str(interaction.guild_id) not in notice:
            return await interaction.response.send_message("공지채널이 설정되지 않았습니다.") # noqa
        if not notice[str(interaction.guild_id)] == 'no':
            channel = bot.get_channel(notice[str(interaction.guild_id)])
            embed = discord.Embed(title=f"{keyword}", description=f"{description}", color=discord.Color.green())
            await channel.send(embed=embed)
            await interaction.response.send_message("공지를 전송했습니다.") # noqa
        else:
            await interaction.response.send_message("공지채널이 설정되지 않았습니다.") # noqa


def load_no_keyword():
    try:
        with open("no_keyword.json'", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def save_no_keyword(no_keyword):
    with open("no_keyword.json", "w") as f:
        json.dump(no_keyword, f, indent=4)


def get_guild_id(ctx):
    return str(ctx.guild.id)


@bot.hybrid_command(name="제재로그설정", description="제재로그 채널을 설정합니다.")
async def set_log(ctx, channel: discord.TextChannel):
    if not check_admin(ctx):
        await ctx.send("권한이 없습니다.")
        return 
    await ctx.send(f"제재로그 채널을 {channel.mention}로 설정했습니다.")
    channels = channel.id
    log_channel = open_log_channel()
    log_channel[str(ctx.guild.id)] = channels
    save_log_channel(log_channel)
    await channel.send(f"{ctx.guild.name} 서버에서 제재로그 채널을 {channel.mention}로 설정했습니다.")


@bot.hybrid_command(name="제재로그해제", description="제재로그 채널을 해제합니다.")
async def remove_log(ctx):
    if not check_admin(ctx):
        await ctx.send("권한이 없습니다.")
        return 
    log_channel = open_log_channel()
    log_channel[str(ctx.guild.id)] = 'no'
    save_log_channel(log_channel)
    await ctx.send("제재로그 채널을 해제했습니다.")


@bot.hybrid_command(name="욕설제재설정", description="욕설 제재를 설정 합니다.")
async def set_warn(ctx):
    if not check_admin(ctx):
        await ctx.send("권한이 없습니다.")
        return 
    swear = open_swear()
    if str(ctx.guild.id) not in swear:
        swear[str(ctx.guild.id)] = True
        save_swear(swear)
        return await ctx.send(f"욕설 제재를 True로 설정했습니다.")
    if swear[str(ctx.guild.id)]:
        swear[str(ctx.guild.id)] = False
        save_swear(swear)
        return await ctx.send(f"욕설 제재를 False로 설정했습니다.")
    else:
        swear[str(ctx.guild.id)] = True
        save_swear(swear)
        return await ctx.send(f"욕설 제재를 True로 설정했습니다.")


@bot.hybrid_command(name="경고부여", description="멤버에게 경고를 부여합니다.")
async def warn(ctx, member: discord.Member, *, warns: int):
    if not check_admin(ctx):
        await ctx.send("권한이 없습니다.")
        return 
    
    log_channel = open_log_channel()
    if str(ctx.guild.id) not in log_channel:
        return await ctx.send("아직 제재로그 채널이 설정되지 않았습니다.")
    if not log_channel[str(ctx.guild.id)] == 'no':
        if warns < 1:
            return await ctx.send("경고는 1 이상으로 설정해주세요.")
        warn = open_warn()
        if str(member.id) not in warn:
            warn[str(member.id)] = 0
        warn[str(member.id)] += warns
        await ctx.send(f"{member.mention}님에게 경고를 부여했습니다.")
        channel = bot.get_channel(log_channel[str(ctx.guild.id)])
        embed = discord.Embed(title=f"경고", description=f"경고 {warns} 부여", color=discord.Color.red())
        embed.add_field(name=f"누적경고수", value=f"{warn[str(member.id)]}", inline=False)
        embed.set_author(name=f"{member}", icon_url=member.avatar)
        await channel.send(embed=embed)
        save_warn(warn)
    else:
        await ctx.send("아직 제재로그 채널이 설정되지 않았습니다.")


@bot.hybrid_command(name="경고회수", description="멤버의 경고를 회수합니다.")
async def remove_warn(ctx, member: discord.Member, *, warns: int):
    if not check_admin(ctx):
        await ctx.send("권한이 없습니다.")
        return 
    log_channel = open_log_channel()
    if str(ctx.guild.id) not in log_channel:
        return await ctx.send("아직 제재로그 채널이 설정되지 않았습니다.")
    if not log_channel[str(ctx.guild.id)] == 'no':
        if warns < 1:
            return await ctx.send("경고는 1 이상으로 설정해주세요.")
        warn = open_warn()
        if str(member.id) not in warn:
            return await ctx.send("해당 멤버는 경고를 받지 않았습니다.")
        if warn[str(member.id)] < warns:
            return await ctx.send("해당 멤버의 경고수보다 더 많은 경고를 회수할 수 없습니다.")
        warn[str(member.id)] -= warns
        await ctx.send(f"{member.mention}님의 경고를 회수했습니다.")
        channel = bot.get_channel(log_channel[str(ctx.guild.id)])
        embed = discord.Embed(title=f"경고", description=f"경고 {warns} 회수", color=discord.Color.red())
        embed.add_field(name=f"누적경고수", value=f"{warn[str(member.id)]}", inline=False)
        embed.set_author(name=f"{member}", icon_url=member.avatar)
        await channel.send(embed=embed)
        save_warn(warn)
    else:
        await ctx.send("아직 제재로그 채널이 설정되지 않았습니다.")


@bot.hybrid_command(name="경고확인", description="멤버의 경고를 확인합니다.")
async def check_warn(ctx, member: discord.Member):
    log_channel = open_log_channel()
    if str(ctx.guild.id) not in log_channel:
        return await ctx.send("아직 제재로그 채널이 설정되지 않았습니다.")
    if not log_channel[str(ctx.guild.id)] == 'no':
        warn = open_warn()
        if str(member.id) not in warn:
            return await ctx.send("해당 멤버는 경고를 받지 않았습니다.")
        await ctx.send(f"{member.mention}님의 경고수는 {warn[str(member.id)]}입니다.")
    else:
        await ctx.send("아직 제재로그 채널이 설정되지 않았습니다.")


@bot.hybrid_command(name="입장로그설정", description="입장로그 채널을 설정합니다.")
async def set_hello_log(ctx, channel: discord.TextChannel):
    if not check_admin(ctx):
        await ctx.send("권한이 없습니다.")
        return 
    await ctx.send(f"입장로그 채널을 {channel.mention}로 설정했습니다.")
    channels = channel.id
    hello_log = open_hello_log()
    hello_log[str(ctx.guild.id)] = channels
    save_hello_log(hello_log)
    await channel.send(f"{ctx.guild.name} 서버에서 입장로그 채널을 {channel.mention}로 설정했습니다.")


@bot.hybrid_command(name="입장로그해제", description="입장로그 채널을 해제합니다.")
async def remove_hello_log(ctx):
    if not check_admin(ctx):
        await ctx.send("권한이 없습니다.")
        return 
    hello_log = open_hello_log()
    hello_log[str(ctx.guild.id)] = 'no'
    save_hello_log(hello_log)
    await ctx.send("입장로그 채널을 해제했습니다.")


@bot.hybrid_command(name='핑', description="퐁!")
async def ping(ctx):
    message_latency = round(bot.latency * 1000, 2)
    start_times = ctx.message.created_at
    message5 = await ctx.send("메시지 핑 측정중...")
    end_time = message5.created_at
    await message5.delete()
    latency = (end_time - start_times).total_seconds() * 1000

    embed = discord.Embed(title="퐁!", color=0xFFB2F5)
    embed.add_field(name=f'REST ping', value=f"`{latency}ms`")
    embed.add_field(name=f'Gateway ping', value=f"`{message_latency}ms`")
    list_length = len(bot.guilds)
    embed.add_field(name="서버수", value=f"`{list_length}`")
    await ctx.send(embed=embed)


@bot.hybrid_command(name="help", description="도움말을 확인합니다.")
async def help(ctx):
    embed = discord.Embed(title="도움말", description="명령어 목록입니다.", color=0xFFB2F5)
    embed.add_field(name="핑", value="퐁!", inline=False)
    embed.add_field(name="제재로그설정", value="제재로그 채널을 설정합니다.", inline=False)
    embed.add_field(name="제재로그해제", value="제재로그 채널을 해제합니다.", inline=False)
    embed.add_field(name="욕설제재설정", value="욕설 제재를 설정 합니다.", inline=False)
    embed.add_field(name="경고부여", value="멤버에게 경고를 부여합니다.", inline=False)
    embed.add_field(name="경고회수", value="멤버의 경고를 회수합니다.", inline=False)
    embed.add_field(name="경고확인", value="멤버의 경고를 확인합니다.", inline=False)
    embed.add_field(name="입장로그설정", value="입장로그 채널을 설정합니다.", inline=False)
    embed.add_field(name="입장로그해제", value="입장로그 채널을 해제합니다.", inline=False)
    embed.add_field(name="help", value="도움말을 확인합니다.", inline=False)
    await ctx.send(embed=embed)


@bot.hybrid_command(name="소개", description="리이봇 소개")
async def introduce(ctx):
    embed = discord.Embed(title="안녕하세요, 리이입니다!", description="봇하나로 쉽게 서버 관리하기, 리이", color=0xFFB2F5)
    embed.set_thumbnail(url="https://cdn.litt.ly/images/eYG6ii7WIWrWNaNO7jdF5qnlV8BMB4yg?s=1280x2400&m=outside&f=webp")
    embed.add_field(name="리이봇", value="리이봇은 서버관리에 특화된 기능을 가지고 있는 서버관리 봇입니다.", inline=False)
    embed.add_field(name="오픈소스", value="© Korcen을 사용하여 욕설제재기능을 개발하였습니다.", inline=False)
    embed.add_field(name="개발자", value="studio boran", inline=False)
    await ctx.send(embed=embed)


@bot.hybrid_command(name="공지채널설정", description="공지채널을 설정합니다.")
async def set_notice(ctx, channel: discord.TextChannel):
    if not check_admin(ctx):
        await ctx.send("권한이 없습니다.")
        return 
    await ctx.send(f"공지채널을 {channel.mention}로 설정했습니다.")
    channels = channel.id
    notice = open_notice()
    notice[str(ctx.guild.id)] = channels
    save_notice(notice)
    await channel.send(f"{ctx.guild.name} 서버에서 공지채널을 {channel.mention}로 설정했습니다.")


@bot.hybrid_command(name="공지채널해제", description="공지채널을 해제합니다.")
async def remove_notice(ctx):
    if not check_admin(ctx):
        await ctx.send("권한이 없습니다.")
        return 
    notice = open_notice()
    notice[str(ctx.guild.id)] = 'no'
    save_notice(notice)
    await ctx.send("공지채널을 해제했습니다.")


@bot.tree.command(name="공지", description="공지를 전송합니다.")
async def notice(interaction: discord.Interaction):
    if not interaction.permissions.administrator:
        await interaction.response.send_message("권한이 없습니다.")# noqa
        return
    notice = open_notice()
    if str(interaction.guild_id) not in notice:
        await interaction.response.send_message("공지채널이 설정되지 않았습니다.")# noqa
        return
    if not notice[str(interaction.guild_id)] == 'no':
        await interaction.response.send_modal(MyModal())# noqa
        return
    else:
        await interaction.response.send("공지채널이 설정되지 않았습니다.")# noqa
        return


@bot.event
async def on_member_join(member):
    hello_log = open_hello_log()
    if str(member.guild.id) not in hello_log:
        return
    if not hello_log[str(member.guild.id)] == 'no':
        channel = bot.get_channel(hello_log[str(member.guild.id)])
        embed = discord.Embed(title=f"입장로그", description=f"{member.mention}님이 입장했습니다.", color=discord.Color.green())
        member = member
        embed.set_author(name=f"{member}", icon_url=member.avatar)
        await channel.send(embed=embed)


@bot.event
async def on_message(message):
    if message.author.bot:
        return
    log_channel = open_log_channel()
    swear = open_swear()
    if str(message.guild.id) not in log_channel:
        log_channel[str(message.guild.id)] = 'no'
    if not log_channel[str(message.guild.id)] == 'no':
        if swear[str(message.guild.id)]:
            messages = message.content.lower()
            if korcen.check(messages):
                await message.delete()
                channel = bot.get_channel(log_channel[str(message.guild.id)])
                await channel.send(f"**{message.author}**님이 **{message.channel}**에서 **{message.content}**라고 말했습니다.")
                embed = discord.Embed(title=f"", description=f"```{message.content}```", color=discord.Color.red())
                member = message.author
                embed.set_author(name=f"{message.author}", icon_url=member.avatar)
                embed.set_footer(text=f"욕은 금지!")
                await channel.send(embed=embed)
    await bot.process_commands(message)


bot.run()
