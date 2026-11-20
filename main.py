import re, json, html, aiohttp, asyncio
from flask import Flask, request, jsonify
from datetime import datetime, timezone, timedelta

class amdtsmodz:
 def __init__(self):
  self.app=Flask(__name__)

 def Sc_amdtsmodz_inf(self,username):
  username=username.strip().lstrip("@")
  if not re.fullmatch(r"[A-Za-z0-9._]{1,24}",username):
   return {"success":False,"error":"Invalid TikTok username."},400
  try:
   async def fetch():
    async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=25)) as s:
     async with s.get(f"https://www.tiktok.com/@{username}",headers={
      "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/131.0.0.0 Safari/537.36",
      "Referer":"https://www.tiktok.com/"
     }) as r:
      if r.status!=200:
       return None,r.status
      return await r.text(),r.status

   page,status=asyncio.run(fetch())
   if status==404:
    return {"success":False,"error":"TikTok account not found."},404
   if status!=200:
    return {"success":False,"error":f"TikTok returned HTTP {status}."},status

   raw=None
   for pattern in (
    r'<script[^>]*id=["\']__UNIVERSAL_DATA_FOR_REHYDRATION__["\'][^>]*>(.*?)</script>',
    r'<script[^>]*id=["\']SIGI_STATE["\'][^>]*>(.*?)</script>'
   ):
    m=re.search(pattern,page,re.S|re.I)
    if m:
     try:
      raw=json.loads(html.unescape(m.group(1)))
      break
     except:
      pass

   if not isinstance(raw,dict):
    return {"success":False,"error":"Unable to retrieve TikTok account data."},502

   info=raw.get("__DEFAULT_SCOPE__",{}).get("webapp.user-detail",{}).get("userInfo",{})
   u=info.get("user",{})
   st=info.get("stats",{})
   st2=info.get("statsV2",{})

   if not u:
    module=raw.get("UserModule",{})
    u=module.get("users",{}).get(username,{})
    st=module.get("stats",{}).get(username,{})
    st2={}

   if not u:
    return {"success":False,"error":"Account information not found."},404

   created=None
   if u.get("createTime"):
    try:
     created=datetime.fromtimestamp(int(u["createTime"]),timezone.utc).astimezone(timezone(timedelta(hours=7))).strftime("%H:%M:%S %d/%m/%Y")
    except:
     created=None

   uid=u.get("uniqueId") or username
   return {
    "success":True,
    "user":{
     "id":u.get("id"),
     "username":uid,
     "nickname":u.get("nickname"),
     "bio":u.get("signature") or "No bio",
     "avatar":u.get("avatarLarger") or u.get("avatarMedium") or u.get("avatarThumb"),
     "private":u.get("privateAccount",False),
     "created":created,
     "followers":st.get("followerCount",st2.get("followerCount",0)),
     "following":st.get("followingCount",st2.get("followingCount",0)),
     "likes":st.get("heartCount",st.get("heart",st2.get("heartCount",st2.get("heart",0)))),
     "videos":st.get("videoCount",st2.get("videoCount",0)),
     "url":f"https://www.tiktok.com/@{uid}"
    }
   },200
  except Exception as e:
   return {"success":False,"error":str(e)[:300]},500

 def run(self):
  @self.app.route("/tiktok",methods=["GET"])
  def tiktok():
   data,status=self.Sc_amdtsmodz_inf(request.args.get("username",""))
   return jsonify(data),status

  self.app.run(host="0.0.0.0",port=5000)

if __name__=="__main__":
 amdtsmodz().run()
