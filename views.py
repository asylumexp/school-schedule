import discord


class TimetableView(discord.ui.View):
    def __init__(self, *, timetable, i, user, timeout=180):
        self.i = i
        self.timetable = timetable
        self.user = user
        super().__init__(timeout=timeout)

    @discord.ui.button(label="Previous Day", style=discord.ButtonStyle.gray)
    async def previous_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if int(self.i) > 0:
            i = int(self.i) - 1
            self.i = str(i)
        await self.replaceEmbed(interaction=interaction, button=button)

    @discord.ui.button(label="Next Show", style=discord.ButtonStyle.gray)
    async def next_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if int(self.i) < 9:
            i = int(self.i) + 1
            self.i = str(i)
        await self.replaceEmbed(interaction=interaction, button=button)

    async def replaceEmbed(self, interaction: discord.Interaction, button: discord.ui.Button):
        emb = discord.Embed(title="Timetable", description=f"Day {self.i}")

        for key in self.timetable[self.user][self.i].keys():

            if self.timetable[self.user][self.i][key]['class']:
                msg = f"{self.timetable[self.user][self.i][key]['class']} in {self.timetable[self.user][self.i][key]['location']}"
            else:
                msg = '-'

            emb.add_field(name=f"Period {key}", value=msg)

        await interaction.response.edit_message(embed=emb, view=TimetableView(timetable=self.timetable, user=self.user, i=self.i))
