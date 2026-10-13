"""Verify the public Pages release after a successful deployment."""
import os,time,urllib.request
base=os.environ.get('SITE_URL','').rstrip('/')
if not base.startswith('https://lichunubc.github.io/'):
    raise SystemExit('Expected the configured public course Pages URL')
checks=[('', 'topic-1-1.html'), ('topic-1-1.html', 'data-foundation="population"')]
for path,marker in checks:
    url=base+'/'+path+'?release='+os.environ.get('GITHUB_SHA','check')
    last=None
    for attempt in range(16):
        try:
            request=urllib.request.Request(url,headers={'User-Agent':'MapleHillCourse-DeploymentCheck'})
            with urllib.request.urlopen(request,timeout=15) as response:
                text=response.read().decode('utf-8')
                assert response.status==200
                assert marker in text, 'Expected chapter content not present yet'
            print('Verified public page:',base+'/'+path)
            break
        except Exception as error:
            last=error
            if attempt<15: time.sleep(5)
    else:
        raise SystemExit(f'Public verification failed for {base}/{path}: {last}')
