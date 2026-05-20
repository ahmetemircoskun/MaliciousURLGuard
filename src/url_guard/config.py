"""Project constants used by both training and the app."""

from __future__ import annotations

RANDOM_STATE = 42
DEFAULT_THRESHOLD = 0.55

SUSPICIOUS_TLDS = {
    ".tk", ".ml", ".ga", ".cf", ".gq", ".xyz", ".top", ".work",
    ".click", ".link", ".pw", ".cc", ".club", ".online", ".site",
    ".store", ".live", ".icu", ".vip", ".buzz", ".cyou", ".monster",
    ".quest", ".rest", ".cam", ".sbs", ".bar",
}

TRUSTED_TLDS = {
    ".com", ".org", ".net", ".edu", ".gov", ".mil", ".io", ".co",
    ".de", ".uk", ".ca", ".au", ".fr", ".nl", ".edu.tr", ".gov.tr",
}

ABUSED_COUNTRY_TLDS = {".ru", ".cn", ".br", ".in", ".pk", ".ng", ".su"}

SHORTENER_DOMAINS = {
    "bit.ly", "goo.gl", "tinyurl.com", "ow.ly", "t.co", "is.gd", "buff.ly",
    "adf.ly", "cutt.ly", "rb.gy", "shorturl.at", "tiny.cc", "lnkd.in",
    "soo.gd", "s2r.co", "rebrand.ly", "bitly.com", "trib.al",
}

SUSPICIOUS_KEYWORDS = [
    "login", "signin", "sign-in", "logon", "log-on", "account", "verify",
    "validate", "update", "confirm", "secure", "security", "banking",
    "payment", "invoice", "password", "credential", "suspend", "limited",
    "alert", "wallet", "recover", "support", "token", "auth", "reset",
    "unlock", "billing", "refund", "webscr", "session", "2fa", "otp",
]

BRANDS = [
    "paypal", "apple", "amazon", "facebook", "microsoft", "netflix",
    "instagram", "twitter", "linkedin", "whatsapp", "bankofamerica",
    "chase", "wellsfargo", "citibank", "hsbc", "dropbox", "icloud",
    "outlook", "office365", "onedrive", "steam", "roblox", "fortnite",
    "google", "youtube", "wikipedia", "github", "stackoverflow", "reddit",
    "bing", "yahoo", "mozilla", "ubuntu", "apache", "oracle", "ibm",
    "nvidia", "adobe", "salesforce", "zoom", "tiktok", "snapchat",
    "pinterest", "twitch", "discord", "spotify", "duckduckgo", "binance",
    "coinbase", "metamask", "visa", "mastercard", "americanexpress",
]

EXECUTABLE_EXTENSIONS = {
    ".exe", ".zip", ".rar", ".bat", ".msi", ".dmg", ".scr", ".jar",
    ".apk", ".cmd", ".ps1", ".iso", ".7z",
}

SCRIPT_EXTENSIONS = {".php", ".asp", ".aspx", ".cgi", ".pl", ".jsp"}
