# LLM-LINEBot-use-python-on-vercel

本專案已經採用OpenAI ChatGPT-3.5-tubo模型，並且針對教育情境優化，詳細描述於[🤖 客製化你的AI教學助手-蘇格拉底引導教學法 (Customize Your AI Teaching Assistant - A Socratic Approach)](https://willismax.github.io/my-site/blog/Customize%20Your%20AI%20Teaching%20Assistant%20-%20A%20Socratic%20Approach)

## ChatGPT on Vercel (Pthon Flask ver.)
- 這個教學可以直接Fork專案部署完成，開發時可以clone到本機，或跟筆者一樣嘗試在 GitHub Codespace 搞定一切。

## 如何使用?
1. 註冊必要平台：包括 [GitHub](https://github.com/)、[Vercel](https://vercel.com/)、[OpenAI API](https://openai.com/blog/openai-api)、[LINE Developers](https://developers.line.biz/zh-hant/)。
2. 取得 `OpenAI API token`
3. 建立 LINE Developer Channel，並取得 `Channel Secret` 、 `Channel Access Token`

4. 在 GitHub Fork 這個專案 -> 在 Vercel 建立專案 -> 輸入環境變數 -> 將 Vercel 的專案 Domain 網址綁定在 LINE Channel Webhook (`vercel的專案網址/webhook`)

5. 加入LINE官方帳號，使用者對話將由 ChatGPT-3.5-tubo回應(LINE自動回應須關閉)。
詳細描述於[部落格](https://willismax.github.io/my-site/blog/Customize%20Your%20AI%20Teaching%20Assistant%20-%20A%20Socratic%20Approach)。

## 客製化
- 如果要客製化在其他應用，在`api/prompt.py`修改`AI_GUIDELINES`後提示文字即可，目前預設為教學用，提示詞為:
    ```
    AI_GUIDELINES = '你是一個AI助教，專門使用蘇格拉底教學法來回答學生的問題，如果有需要，會建議學生與老師進一步確認。'
    ``` 
    組合起來就是提示系統:`messages: [{ role: "system", content: "你是一個AI助教，專門使用蘇格拉底教學法來回答學生的問題，如果有需要，會建議學生與老師進一步確認" }]` 
- 請留意 Vercel 有處理超過10秒會Time Out的限制，太複雜可能會逾時。

## 成果展示
-   **出色的問答回應**: 這個AI助手採用ChatGPT 3.5 Tubo，能在精確及速度獲得很好的平衡，即時地回應學生的問題。 ![出色回應](https://hackmd.io/_uploads/ryjveAW-T.png)
-   **問題過濾**: 對於需要更深層次討論的問題，AI助手會提供適當的處理建議，協助老師過濾和分類問題，同時也啟發老師改進教學。 ![問題過濾](https://hackmd.io/_uploads/SkaDCWzbp.png)
-   **引導學生思考**: 透過蘇格拉底教學法，AI助手不僅回答問題，還能引導學生學會如何提問和解決問題。 

    ![培養思考](https://hackmd.io/_uploads/ryjTiWfZT.png) ![成果展示](https://hackmd.io/_uploads/HkZ1nWzbp.png) ![更多示例](https://hackmd.io/_uploads/Byyf2bGWp.png)

## 顯示加載動畫
-   **加載動畫**: 此功能允許LINE用戶界面使用提供的curl命令顯示加載動畫。動畫在處理消息之前觸發，向用戶提供其請求正在處理的視覺指示。

    啟動加載動畫的示例curl命令：
    ```
    curl -v -X POST https://api.line.me/v2/bot/chat/loading/start \
    -H 'Content-Type: application/json' \
    -H 'Authorization: Bearer {channel access token}' \
    -d '{
        "chatId": "U4af4980629...",
        "loadingSeconds": 5
    }'
    ```
