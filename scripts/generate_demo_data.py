"""
ScamShield AI - Synthetic Dataset Generation Script
RAKSHAM AI Cybersecurity Hackathon | IIT Delhi (Problem Statement 2)
"""

import os
import csv
import random

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
CSV_PATH = os.path.join(DATA_DIR, "synthetic_messages.csv")

# Set deterministic random seed
random.seed(42)

# --- 1. SCAM SAMPLES ---
SCAM_TEMPLATES = [
    # KYC & Bank Suspension Scams
    ("Dear SBI Customer, your YONO account is suspended today due to KYC pending. Click http://sbi-kyc-verify.xyz to update immediately.", "KYC Phishing", "http://sbi-kyc-verify.xyz"),
    ("HDFC Bank Alert: Your netbanking will be blocked within 24 hours. Update your PAN card details immediately at http://hdfc-pan-update.top/login", "KYC Phishing", "http://hdfc-pan-update.top/login"),
    ("ICICI Alert: Your credit card is deactivated. Verify your identity now at http://icici-card-active.site to avoid permanent closure.", "KYC Phishing", "http://icici-card-active.site"),
    ("Axis Bank Notice: Complete your mandatory KYC verification today itself by visiting http://axis-kyc-portal.club or account will be frozen.", "KYC Phishing", "http://axis-kyc-portal.club"),
    ("PNB Alert: Your debit card has been blocked due to suspicious activity. Click http://192.168.1.105/pnb-unblock to restore access.", "KYC Phishing", "http://192.168.1.105/pnb-unblock"),
    ("Kotak Mahindra: Your 811 account is blocked. Update Aadhaar and PAN immediately at http://kotak-aadhaar-link.xyz before midnight.", "KYC Phishing", "http://kotak-aadhaar-link.xyz"),
    ("Bank of Baroda: Important! Your account is temporarily suspended. Click http://bob-verify.online to submit your documents immediately.", "KYC Phishing", "http://bob-verify.online"),
    ("Canara Bank Alert: Immediate action required. Update your KYC details at http://canarabank-kyc.link within 12 hours.", "KYC Phishing", "http://canarabank-kyc.link"),
    ("Union Bank: Your netbanking password expired. Renew your login credentials at http://unionbank-secure.vip immediately.", "KYC Phishing", "http://unionbank-secure.vip"),
    ("Dear customer, your bank account will be closed today. Turant kyc update karein http://bank-kyc-now.site par.", "KYC Phishing (Hinglish)", "http://bank-kyc-now.site"),

    # Digital Arrest & Law Enforcement Extortion
    ("CBI Cyber Crime Cell: A parcel containing narcotics registered on your Aadhaar was intercepted at Mumbai Airport. You are placed under digital arrest on Skype video call. Stay on call or police team will arrest you.", "Digital Arrest Extortion", None),
    ("Cyber Police Headquarters: Non-bailable arrest warrant issued against your mobile number for illicit money laundering. Connect to officer on WhatsApp video call immediately. Do not disconnect call.", "Digital Arrest Extortion", None),
    ("Customs Department Notice: Contraband goods and foreign currency seized in international package #IND8892 under your PAN. Contact Narcotics Bureau Officer on WhatsApp immediately to avoid FIR.", "Digital Arrest Extortion", None),
    ("Enforcement Directorate (ED): Your bank accounts are frozen under PMLA. Join confidential Skype video interrogation room immediately to record statement.", "Digital Arrest Extortion", None),
    ("Mumbai Crime Branch: Illegal parcel intercepted with passport copy. Turant WhatsApp video call pe judiye aur call disconnect mat karna.", "Digital Arrest Extortion (Hinglish)", None),

    # Investment & Stock Ponzi Scams
    ("VIP Institutional Stock Group: Guaranteed 500% returns in 7 days on pre-allotted IPO stocks. Join our exclusive WhatsApp trading channel @WealthVIP to start with Rs 5,000.", "Investment Ponzi Scam", None),
    ("Earn 200% daily profit on automated crypto arbitrage trading. Double your investment safely within 48 hours. Message Senior Analyst on WhatsApp at 9876541230.", "Investment Ponzi Scam", None),
    ("Exclusive SEBI Insider Club: Daily guaranteed profit of Rs 15,000 with zero risk. Join our private Telegram channel @DailyProfitIndia.", "Investment Ponzi Scam", None),
    ("Ghar baithe 5000 rupaye daily double kare. Share market VIP tips prapt karne ke liye WhatsApp kare 9811223344.", "Investment Ponzi Scam (Hinglish)", None),

    # UPI & Cashback Scams
    ("Congratulations! You won ₹5,000 PhonePe festive cashback. Click http://phonepe-reward-claim.xyz and enter your UPI PIN to claim money.", "UPI Fraud", "http://phonepe-reward-claim.xyz"),
    ("Google Pay Reward: You have received a scratch card of Rs 2,500. Scan QR code and enter UPI PIN to receive money in bank account.", "UPI Fraud", None),
    ("Paytm Cashback: Rs 1,999 credited to your wallet. Approve the UPI collect request in Paytm app to receive funds instantly.", "UPI Fraud", None),
    ("BHIM UPI: You have received Rs 10,000 from customer support. Enter UPI PIN to verify your account and receive payment.", "UPI Fraud", None),
    ("Cred Reward: Claim your exclusive jackpot reward of Rs 7,500. Send Re 1 verification token to rewards@okaxis to unlock prize.", "UPI Fraud", None),
    ("Apna PhonePe cashback prapt karne ke liye turant collect request approve kare aur PIN enter kare.", "UPI Fraud (Hinglish)", None),
    ("Dear user, ₹3,500 cashback is waiting in your GPay account. Enter your UPI MPIN immediately to credit your savings account.", "UPI Fraud", None),
    ("Instant UPI refund: Send Rs 1 to refund-verify@paytm to initiate automated reversal of your failed transaction.", "UPI Fraud", None),
    ("OLX Buyer: I am sending advance payment of Rs 12,000 for your furniture. Scan this QR code in GPay and enter your UPI PIN to credit funds in account.", "UPI Fraud", None),

    # Electricity & Utility Scams
    ("Dear Consumer, your electricity power will be disconnected tonight at 9:30 PM from power office because bill not updated. Call 9876543210 immediately.", "Electricity Scam", None),
    ("BSES Alert: Your electricity power supply will be cut off tonight. Contact Electricity Officer at 9811223344 immediately to avoid disconnection.", "Electricity Scam", None),
    ("Mahadiscom notice: Electricity bill unpaid. Power disconnected tonight at 10 PM. Call our executive 9988776655 right now.", "Electricity Scam", None),
    ("Tata Power: Immediate disconnection notice. Pay previous month bill before 9:30 PM by calling 9765432109.", "Electricity Scam", None),
    ("UPPCL Bijli Bill: Bijli ka bill jama na hone ke karan aaj raat 9:30 baje bijli kaat di jayegi. Turant sampark kare 9876501234.", "Electricity Scam (Hinglish)", None),
    ("DHBVN Electricity Board: Your connection is scheduled for cutoff tonight. Contact officer on 9845123456 to clear dues.", "Electricity Scam", None),
    ("CESC Urgent: Power disconnection order issued for your meter. Call nodal officer 9830123456 immediately.", "Electricity Scam", None),
    ("Dear consumer your electricity power will be disconnected at 9.30 pm from electricity office because your previous month bill was not update please immediately contact our power officer 9876543210", "Electricity Scam", None),

    # Remote Access & Support Scams
    ("Paytm Support: To resolve your failed transaction of Rs 1,450, install AnyDesk app from Play Store and share the 9-digit code.", "Remote Access Scam", None),
    ("Bank Helpdesk: Install TeamViewer QuickSupport on your mobile phone so our senior engineer can fix your transaction timeout.", "Remote Access Scam", None),
    ("Google Pay Executive: Please download RustDesk application to assist you with KYC document synchronization.", "Remote Access Scam", None),
    ("Customer Care: To process instant refund, install Zoho Assist remote software and connect with our live technical agent.", "Remote Access Scam", None),
    ("Airtel Payments Bank: Download QuickSupport app immediately to complete your biometric fingerprint registration remotely.", "Remote Access Scam", None),

    # Unofficial APK & Malware
    ("Dear SBI user, download the updated SBI YONO 2.0 app from http://sbi-app-update.top/yono.apk to continue using mobile banking.", "Malware/APK Scam", "http://sbi-app-update.top/yono.apk"),
    ("Income Tax Refund: Tax refund of Rs 18,540 approved. Download IT-Refund app from http://incometax-filing.site/tax.apk to claim.", "Malware/APK Scam", "http://incometax-filing.site/tax.apk"),
    ("PAN Aadhaar Link: Mandatory verification. Install government linking app from http://pan-link-gov.online/pan.apk today.", "Malware/APK Scam", "http://pan-link-gov.online/pan.apk"),
    ("WhatsApp Gold Update: Upgrade to premium edition with exclusive features by installing http://whatsapp-gold.club/app.apk", "Malware/APK Scam", "http://whatsapp-gold.club/app.apk"),

    # Job & Task Scams
    ("Part-time job offer: Earn Rs 3,000 to Rs 8,000 daily by liking YouTube videos from home. Join our Telegram channel @DailyEarnIndia.", "Job Scam", None),
    ("Work from home opportunity: Simple typing and review task. Daily payout Rs 5,000. Message HR on WhatsApp at 9876123456.", "Job Scam", None),
    ("Amazon Task Hiring: Earn daily salary of Rs 4,500. Deposit Rs 500 registration fee to activate VIP prepaid tasks on Telegram.", "Job Scam", None),
    ("Ghar baithe kamaye 5000 rupaye daily. YouTube video like kare aur paise kamaye. WhatsApp kare 9812345678.", "Job Scam (Hinglish)", None),
    ("Flipkart Affiliate hiring: Earn 50k monthly. Join Telegram group @FlipkartTasks to receive daily payment tasks.", "Job Scam", None),
    ("Google Maps Review Job: Earn Rs 500 per 5-star review. Daily earnings Rs 4,500. Message HR on Telegram @GoogleReviewTasks.", "Job Scam", None),

    # Courier & Customs Scams
    ("FedEx Alert: Your parcel #FDX8910 is detained at Mumbai Customs due to suspicious items. Pay clearance duty of Rs 1,200 at http://fedex-customs.xyz", "Courier Scam", "http://fedex-customs.xyz"),
    ("India Post: Your package could not be delivered due to incomplete address. Update delivery address within 24 hours at http://indiapost-update.top", "Courier Scam", "http://indiapost-update.top"),
    ("DHL Express: Parcel on hold due to unpaid customs fee of Rs 450. Click http://dhl-parcel-track.site to release shipment.", "Courier Scam", "http://dhl-parcel-track.site"),
    ("Customs Department Notice: A legal notice has been issued against parcel #CT9910. Contact Narcotics Bureau officer immediately.", "Courier Scam", None),

    # Lottery & Prize Scams
    ("KBC Lucky Draw: Congratulations! Your mobile number has won Rs 25,00,000 in KBC lottery. Contact Rana Pratap Singh on WhatsApp 9876543210 to claim.", "Lottery Scam", None),
    ("Congratulations! You are selected for Tata Safari car lucky draw prize. Call 9811223344 to pay processing charges and claim vehicle.", "Lottery Scam", None),
    ("Aapka mobile number KBC lottery me chuna gaya hai. 25 lakh ka inaam prapt karne ke liye WhatsApp kare 9988776655.", "Lottery Scam (Hinglish)", None)
]

# --- 2. BENIGN SAMPLES ---
BENIGN_TEMPLATES = [
    # Automated Bank Transaction Alerts
    ("Your A/c XX4521 is credited with INR 65,000.00 on 05-OCT-2026 by NEFT salary transfer. Avl Bal: INR 78,420.50 - SBI", "Benign Banking", None),
    ("INR 450.00 debited from A/c XX8910 on 08-OCT-2026 at Swiggy UPI. Txn Ref 9081234567. Avl Bal: INR 12,340.00 - HDFC Bank", "Benign Banking", None),
    ("Your A/c XX1209 is debited by INR 2,000.00 on 09-OCT-2026 at ATM Cash Withdrawal. Avl Bal: INR 34,100.00 - ICICI Bank", "Benign Banking", None),
    ("Dear Customer, INR 15,000.00 credited to your A/c XX7722 via IMPS Ref 89012345. - Axis Bank", "Benign Banking", None),
    ("Kotak Bank: Rs 1,299.00 paid towards electricity bill ref #908123. Available balance: Rs 45,900.00.", "Benign Banking", None),
    ("Punjab National Bank: A/c *8890 debited for Rs 850.00 on 10-OCT-2026 at D-Mart POS. Avl Bal: Rs 8,450.00.", "Benign Banking", None),
    ("Bank of Baroda: Your monthly interest of INR 245.00 has been credited to your savings account *3412.", "Benign Banking", None),
    ("A/c XX9910 credited with INR 500.00 from rahul@okhdfcbank via UPI. Avl Bal: INR 5,420.00 - Paytm Payments Bank", "Benign Banking", None),

    # Official Bank Fraud Alerts with 1800 Toll-Free Helplines & SMS Block Shortcodes (Challenging Benign)
    ("SBI Security Alert: Unauthorised transaction of INR 45,000.00 attempted on card XX4912. If not done by you, call 1800-11-2211 or SMS BLOCK to 567676 immediately to protect your card.", "Benign Security Alert", None),
    ("HDFC Bank Alert: Suspicious login attempt detected on your NetBanking. If not you, call 1800 202 6161 or visit your nearest branch.", "Benign Security Alert", None),
    ("ICICI Bank: OTP for transaction of Rs 12,500 at Croma is 749201. Bank never asks for OTP or CVV. If not done by you, SMS STOP to 561616.", "Benign Security Alert", None),
    ("Axis Bank Fraud Control: Card XX8819 blocked temporarily due to multiple failed ATM attempts. Call 1800-419-5959 to unblock card safely.", "Benign Security Alert", None),
    
    # Official Bank OTPs with Explicit Security Warnings
    ("OTP for online transaction of INR 2,499.00 at Amazon India is 584920. Bank never asks for OTP or password. Do not share OTP with anyone - HDFC Bank", "Benign Security Advisory", None),
    ("590123 is your OTP to login to SBI Internet Banking. Valid for 10 mins. Do NOT share this OTP with anyone, including bank officials.", "Benign Security Advisory", None),
    ("Your ICICI Bank OTP for Net Banking login is 894312. Never share your OTP, password, or CVV with anyone. Stay safe from fraud.", "Benign Security Advisory", None),
    ("674902 is your verification code for PhonePe. Do not share this code with anyone. PhonePe staff will never call asking for OTP.", "Benign Security Advisory", None),
    ("Axis Bank Advisory: Dear Customer, beware of fraudulent calls and SMS asking for KYC updates or remote app installation. Bank never asks for sensitive details.", "Benign Security Advisory", None),

    # Legitimate E-Commerce / Courier In-Person Delivery PINs (Challenging Benign)
    ("Flipkart: Your package containing 'Wireless Mouse' is out for delivery today with partner Sunil (9876543210). Share delivery verification PIN 8492 with agent at the time of delivery.", "Benign Delivery", None),
    ("Amazon: Your order will be delivered today by courier partner. Delivery PIN is 3918. Share only with Amazon delivery associate upon physical handover of parcel.", "Benign Delivery", None),
    ("Zomato: Amit is on his way with your food order. Share delivery PIN 5812 upon arrival.", "Benign Delivery", None),
    ("Swiggy: Your grocery order will be delivered in 10 mins. Share PIN 4910 with delivery partner at your doorstep.", "Benign Delivery", None),
    ("Uber: Your ride with driver Ramesh (DL 1Y 8921) is arriving in 3 mins. PIN is 4819.", "Benign Delivery", None),

    # Legitimate Scheduled Utility Bill Reminders with Official Portals (Challenging Benign)
    ("Dear Consumer, your BSES Rajdhani electricity bill of Rs 1,450.00 for CA #100234567 is due on 18-OCT-2026. Pay online at www.bsesdelhi.com to avail 1% rebate.", "Benign Utility Reminder", "http://www.bsesdelhi.com"),
    ("Tata Power-DDL: Bill for CA 6001298471 of Rs 2,890 is generated. Due date: 20-OCT. Pay via Tata Power Mobile App or netbanking to avoid late surcharge.", "Benign Utility Reminder", None),
    ("Mahadiscom: Electricity bill for Consumer No 01928374 of Rs 850 is due on 22-OCT. Pay online on www.mahadiscom.in to avoid late surcharge.", "Benign Utility Reminder", "http://www.mahadiscom.in"),

    # Legitimate Peer-to-Peer / Family UPI Requests (Challenging Benign)
    ("Hi Dad, I sent a GPay collect request for Rs 1,500 for college semester textbook fees. Please approve when you are free.", "Benign Peer UPI", None),
    ("Hey Priya, requested Rs 450 on PhonePe for yesterday's dinner bill split. Thanks!", "Benign Peer UPI", None),

    # Normal Personal, Academic & Business Communications
    ("Hi Rohit, please review the quarterly budget spreadsheet before our team call at 3 PM today. Thanks.", "Benign General", None),
    ("Dear student, your library book 'Database System Concepts' is due for return on 15-Oct-2026. Please return on time.", "Benign General", None),
    ("Meeting reminder: Project sprint retrospective scheduled for tomorrow at 11:00 AM on Google Meet.", "Benign General", None),
    ("Hey, did you reach home safely? Let me know when you are free to discuss the hackathon project plan.", "Benign General", None),
    ("Your appointment with Dr. Sharma is confirmed for 12-Oct-2026 at 5:30 PM at City Hospital.", "Benign General", None),
    ("IRCTC Booking: PNR 2849018274 confirmed for Train 12951. Coach B3, Berth 45. Happy Journey.", "Benign General", None),
    ("Airtel: Your recharge of Rs 299 is successful. 1.5GB/day data, unlimited calls, valid for 28 days.", "Benign General", None),
    ("IIT Delhi Notice: End-semester course registration closes tonight at 11:59 PM. Please verify your course enrollments on the student ERP portal.", "Benign General", None),
    ("HR Team Reminder: Please submit your health insurance declaration form before 15-Oct-2026 on the corporate intranet.", "Benign General", None),

    # Ambiguous Urgency (Benign context with urgent words)
    ("Urgent: Please submit the final hackathon presentation deck before 6 PM today so the team can review.", "Ambiguous Benign", None),
    ("Immediate action required: The office server maintenance starts at 11 PM tonight. Please save all work.", "Ambiguous Benign", None),
    ("Urgent reminder: Doctor consultation starts in 15 minutes. Please proceed to Room 204.", "Ambiguous Benign", None),
    ("Important notice: College campus will remain closed tomorrow due to heavy rain forecast.", "Ambiguous Benign", None),
    ("Please complete your online course assignment before midnight today to receive the completion certificate.", "Ambiguous Benign", None)
]


def generate_dataset():
    """Generates a balanced dataset of 160+ synthetic records with train/test splits."""
    os.makedirs(DATA_DIR, exist_ok=True)
    all_rows = []
    row_id = 1

    # Expand scam templates with natural variations
    for text, category, url in SCAM_TEMPLATES:
        all_rows.append({
            "id": f"MSG-SCAM-{row_id:04d}",
            "text": text,
            "label": 1,
            "category": category,
            "url": url or ""
        })
        row_id += 1

        # Add duplicate/variation records to test robustness
        variations = [
            text.replace("immediately", "urgently").replace("today", "right now"),
            text.upper() if len(text) < 120 else text.lower()
        ]
        for var in variations:
            all_rows.append({
                "id": f"MSG-SCAM-{row_id:04d}",
                "text": var,
                "label": 1,
                "category": category,
                "url": url or ""
            })
            row_id += 1

    # Expand benign templates
    for text, category, url in BENIGN_TEMPLATES:
        all_rows.append({
            "id": f"MSG-BENIGN-{row_id:04d}",
            "text": text,
            "label": 0,
            "category": category,
            "url": url or ""
        })
        row_id += 1

        # Add natural variations
        variations = [
            text.replace("INR", "Rs.").replace("today", "tonight"),
            text.replace("credited", "received").replace("debited", "spent")
        ]
        for var in variations:
            all_rows.append({
                "id": f"MSG-BENIGN-{row_id:04d}",
                "text": var,
                "label": 0,
                "category": category,
                "url": url or ""
            })
            row_id += 1

    # Shuffle deterministically
    random.shuffle(all_rows)

    # Assign 80% train, 20% test split
    total = len(all_rows)
    split_idx = int(total * 0.80)

    for i, r in enumerate(all_rows):
        r["split"] = "train" if i < split_idx else "test"

    # Write to CSV
    fieldnames = ["id", "text", "label", "category", "url", "split"]
    with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_rows)

    print(f"Generated {len(all_rows)} synthetic messages ({split_idx} train, {total - split_idx} test) at: {CSV_PATH}")


if __name__ == "__main__":
    generate_dataset()
