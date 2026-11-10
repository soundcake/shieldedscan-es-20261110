from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import html, json, shutil

ROOT = Path(__file__).parent
OUT = ROOT / 'shieldedscan-spanish'
OUT.mkdir(exist_ok=True)
FONTS = ROOT / 'fonts'
BG, PANEL, GREEN, WHITE, INK, MUTED = '#050805', '#0a120a', '#2bff64', '#f2fff5', '#d9ffe4', '#7fbf93'
W,H = 1600,1000
panels=[]

def start(n, topic, title, sub):
 global im,draw,svg
 im=Image.new('RGB',(W,H),BG);draw=ImageDraw.Draw(im)
 svg=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">', '<style>@font-face{font-family:JB;src:url(../fonts/JetBrainsMono-Regular.ttf)}@font-face{font-family:JB;src:url(../fonts/JetBrainsMono-Bold.ttf);font-weight:700}</style>']
 rect(0,0,W,H,BG)
 text(80,60,'ZCASH / GUÍA VISUAL',22,MUTED)
 text(1345,60,f'0{n} / 04',22,GREEN)
 line(80,110,1520,110,'#0f4d24',2)
 text(80,160,topic,24,GREEN)
 text(80,215,title,58,WHITE,True)
 text(80,302,sub,26,INK)
 line(80,895,1520,895,'#0f4d24',2)
 text(80,930,'FUENTE: shieldedscan.xyz',20,MUTED)
 text(1100,930,'DATOS PÚBLICOS',20,MUTED)

def text(x,y,s,size=28,color=INK,bold=False):
 font=ImageFont.truetype(str(FONTS/('JetBrainsMono-Bold.ttf' if bold else 'JetBrainsMono-Regular.ttf')),size)
 assert x+draw.textlength(s,font=font)<=W-65,(s,x,size)
 draw.text((x,y),s,font=font,fill=color,anchor='lt')
 svg.append(f'<text x="{x}" y="{y+size*.79}" font-family="JB,monospace" font-size="{size}" font-weight="{700 if bold else 400}" fill="{color}">{html.escape(s)}</text>')

def rect(x,y,w,h,fill,outline=None,radius=0):
 draw.rounded_rectangle((x,y,x+w,y+h),radius=radius,fill=fill,outline=outline,width=2)
 svg.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" fill="{fill}" stroke="{outline or "none"}" stroke-width="2"/>')

def line(x1,y1,x2,y2,color=GREEN,width=3):
 draw.line((x1,y1,x2,y2),fill=color,width=width)
 svg.append(f'<path d="M{x1},{y1} L{x2},{y2}" fill="none" stroke="{color}" stroke-width="{width}"/>')

def finish(n,slug,source):
 name=f'{n:02d}-{slug}'
 im.save(OUT/(name+'.png'))
 (OUT/(name+'.svg')).write_text('\n'.join(svg+['</svg>']))
 panels.append({'number':n,'png':name+'.png','editable_svg':name+'.svg','source':source,'size':[W,H]})

start(1,'> CONOCE EL EXPLORADOR','Zcash, a la vista','Explora datos públicos de la red con ./shieldedscan.')
rect(80,400,1440,420,PANEL,'#0f4d24',20)
text(130,445,'BLOQUES',25,GREEN,True)
for x,label in [(130,'ANTERIOR'),(570,'RECIENTE'),(1010,'SIGUIENTE')]:
 rect(x,510,350,135,BG,'#17a344',12);text(x+30,558,label,30,WHITE,True)
 if x<1000:line(x+350,577,x+440,577)
text(130,700,'Consulta bloques, transacciones y analítica.',30)
text(130,755,'Una interfaz para explorar la actividad de Zcash.',25,MUTED)
finish(1,'explorador','https://shieldedscan.xyz/')

start(2,'> EMPIEZA EN LA PÁGINA PRINCIPAL','Sigue la actividad','Los listados recientes son un punto de entrada a la red.')
for y,n,title,body in [(410,'01','Bloques recientes','Abre un bloque desde el listado.'),(560,'02','Transacciones recientes','Sigue un enlace para consultar su detalle.'),(710,'03','Búsqueda de la cadena','Usa el acceso de búsqueda del explorador.')]:
 rect(80,y,1440,130,PANEL,'#0f4d24',12)
 text(115,y+42,n,36,GREEN,True);text(220,y+22,title,32,WHITE,True);text(220,y+76,body,25,INK)
finish(2,'actividad','https://shieldedscan.xyz/')

start(3,'> ANALÍTICA DE POOLS','Entiende la distribución','La vista de pools muestra cómo se distribuye ZEC en la red.')
for x,title,label in [(80,'Transparent','POOL PÚBLICO'),(575,'Ironwood','POOL BLINDADO'),(1070,'Sapling','POOL BLINDADO')]:
 rect(x,430,450,210,PANEL,'#0f4d24',14);text(x+30,470,title,34,WHITE,True);text(x+30,555,label,22,MUTED)
rect(80,690,1440,150,PANEL,'#17a344',14)
text(115,722,'IRONWOOD: SOLO SU TOTAL ES PÚBLICO',30,GREEN,True)
text(115,780,'Un total agregado no revela los importes de cada operación.',25,INK)
finish(3,'pools','https://shieldedscan.xyz/shielded')

start(4,'> HERRAMIENTAS PARA DESARROLLADORES','Consulta la API','HTTP sin registro ni clave para acceder a datos públicos.')
rect(80,410,1440,120,PANEL,'#17a344',14)
text(120,453,'https://api.shieldedscan.xyz',36,WHITE,True)
for x,y,title in [(80,580,'Bloques'),(820,580,'Transacciones'),(80,700,'Búsqueda'),(820,700,'Suministro y pools')]:
 rect(x,y,700,90,PANEL,'#0f4d24',12);text(x+30,y+28,title,30,INK)
text(80,835,'Consulta /api-docs: rutas, convenciones y límites.',23,MUTED)
finish(4,'api','https://shieldedscan.xyz/api-docs')

(OUT/'manifest.json').write_text(json.dumps({'language':'es','panels':panels,'source_type':'editable SVG text and geometry','brand_source':'https://shieldedscan.xyz/brand','dynamic_chain_values_used':False,'published':False},ensure_ascii=False,indent=2)+'\n')
contact=Image.new('RGB',(1600,1000),BG)
for i,p in enumerate(panels):
 with Image.open(OUT/p['png']) as panel:contact.paste(panel.resize((800,500)),((i%2)*800,(i//2)*500))
contact.save(OUT/'contact-sheet.png')
print(json.dumps({'panels':len(panels),'output':str(OUT),'files':[p.name for p in OUT.iterdir()]}))
