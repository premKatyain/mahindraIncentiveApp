from flask import Flask, render_template, request
import os, random

app = Flask(__name__)

# Load background image paths
BG_FOLDER = os.path.join("static", "backgrounds")
#bg_images = [f"backgrounds/{img}" for img in os.listdir(BG_FOLDER) if img.endswith(('.jpg', '.png'))]

def support(cp, sp, max_dis, ens_margin):
    try:
        margin = ((sp - cp) * 100) / cp
        if margin < ens_margin:
            incent = ens_margin - margin
            if abs(margin) > ens_margin or incent >= max_dis:
                return max_dis
            return round(incent, 4)
        else:
            return 0
    except ZeroDivisionError:
        return "CP cannot be zero!"

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    amount = None
    message = ""
    rating = None
    cp = sp = ens_margin = max_dis = 0.0
    #bg_image = random.choice(bg_images)

    if request.method == "POST":
        try:
            cp = float(request.form["cp"])
            sp = float(request.form["sp"])
            rating=request.form.get('product','')
            if rating=='30':
                ens_margin=3
                max_dis=7
            if rating in ['58.5','62.5','125']:
                ens_margin=3
                max_dis=4
            if rating in ['250','350']:
                ens_margin=2
                max_dis=4
            if rating=='200':
                ens_margin=2.5
                max_dis=4

            incentive = support(cp, sp, max_dis, ens_margin)

            if isinstance(incentive, str):
                message = incentive
            elif incentive == -1:
                message = "❌ Incentive required exceeds maximum allowed discount."
            elif incentive == 0:
                message = "✅ No incentive needed. Margin is already sufficient."
            else:
                result = incentive
                amount = round((incentive * cp) / 100, 2)

        except ValueError:
            message = "Please enter valid numbers."

    return render_template("index.html",product=rating,
                           cp=cp, sp=sp, ens_margin=ens_margin, max_dis=max_dis,
                           result=result, amount=amount, message=message)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Get PORT from environment, fallback to 5000
    app.run(host="0.0.0.0", port=port)

