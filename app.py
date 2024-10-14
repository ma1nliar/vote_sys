from flask import Flask, render_template, request, redirect, url_for, flash
from utils.rsa_utils import generate_keys, sign_message, verify_signature,reconstruct_private_key
from utils.vote_utils import register_voter, cast_vote, get_results

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# In-memory storage
voters = {}
votes = {}
global ppp,qqq
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'register' in request.form:
            voter_id = request.form.get('voter_id', '').strip()
            if voter_id and voter_id not in voters:
                # 生成公钥和私钥
                public_key, private_key = generate_keys()
                voters[voter_id] = {'public_key': public_key, 'private_key': private_key}

                # 获取私钥的 d 和 n 值
                d = private_key['d']
                n = private_key['n']
                global ppp
                global qqq
            
                ppp = private_key['p']
                qqq = private_key['q']

                # 通过 flash 或者 render_template 向前端传递 d 和 n
                

                # 通过 JS 自动填充 d 和 n
                return render_template('index.html', voters=voters, votes=votes, d=d, n=n)
            else:
                flash('该用户已注册或ID无效！', 'warning')
        elif 'vote' in request.form:
            voter = request.form.get('voter', '').strip()
            candidate = request.form.get('candidate', '').strip()
            try:
                d = int(request.form.get('private_key_d').strip())
                n = int(request.form.get('private_key_n').strip())
            except ValueError:
                flash('无效的私钥输入！', 'danger')
                return redirect(url_for('index'))
           
            
            

            if voter in voters:
                # 获取用户输入的私钥
                private_key = reconstruct_private_key(d, n, ppp, qqq)

                # 创建消息并进行签名
                message = f"{voter}:{candidate}"
                try:
                    signature = sign_message(message, private_key)
                except OverflowError as e:
                    flash(f'签名时发生错误: {str(e)}', 'danger')
                    return redirect(url_for('index'))
                flash('success','success')

                # 验证签名
                if verify_signature(message, signature, voters[voter]['public_key']):
                    if voter not in votes:
                        cast_vote(voter, candidate, votes)
                        flash(f'投票成功！您投给了 {candidate}', 'success')
                    else:
                        flash('您已经投过票了！', 'warning')
                else:
                    flash('投票验证失败！', 'danger')
            else:
                flash('用户未注册！', 'danger')

    return render_template('index.html', voters=voters, votes=votes)


@app.route('/results')
def results():
    results = get_results(votes)
    return render_template('results.html', results=results)

if __name__ == '__main__':
    app.run(debug=True)
