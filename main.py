import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

katilimcilar = set()
yonetici_id = None

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global yonetici_id
    if yonetici_id is None:
        yonetici_id = update.effective_user.id
        
    klavye = [[InlineKeyboardButton("🎉 Çekilişe Katıl", callback_data="katil")]]
    cevap_maskesi = InlineKeyboardMarkup(klavye)
    
    await update.message.reply_text(
        "🎁 **Büyük Çekiliş Başladı!**\n\nKatılmak için aşağıdaki butona tıklamanız yeterlidir.",
        reply_markup=cevap_maskesi,
        parse_mode="Markdown"
    )

async def buton_tiklama(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    kullanici = query.from_user
    kullanici_bilgisi = f"@{kullanici.username}" if kullanici.username else kullanici.first_name
    
    if kullanici_bilgisi in katilimcilar:
        await context.bot.send_message(chat_id=kullanici.id, text="Zaten çekilişe katıldınız! ❌")
    else:
        katilimcilar.add(kullanici_bilgisi)
        await context.bot.send_message(chat_id=kullanici.id, text="Çekilişe başarıyla katıldınız! 🎉")

async def kazanan_sec(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != yonetici_id:
        await update.message.reply_text("Bu komutu sadece çekilişi başlatan yönetici kullanabilir! ⛔")
        return
        
    if not katilimcilar:
        await update.message.reply_text("Henüz hiç katılımcı yok! 🤷‍♂️")
        return
        
    kazanan = random.choice(list(katilimcilar))
    await update.message.reply_text(f"🥳 **ÇEKİLİŞ SONUÇLANDI!** 🥳\n\nŞanslı Kazanan: **{kazanan}** \nTebrikler!")

def main():
    TOKEN = "8970510510:AAHQhF_-htOEdW3PLzybNPaPPw9HxJEOwLE"
  
    app = Application.builder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("cekilis_yap", kazanan_sec))
    app.add_handler(CallbackQueryHandler(buton_tiklama, pattern="katil"))
    
    print("Bot aktif...")
    app.run_polling()

if __name__ == "__main__":
    main()
  
