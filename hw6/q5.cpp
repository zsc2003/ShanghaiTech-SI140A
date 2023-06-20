#include<bits/stdc++.h>
#define ll long long
using namespace std;
inline int read()
{
	int r,s=0,c;
	for(;!isdigit(c=getchar());s=c);
	for(r=c^48;isdigit(c=getchar());(r*=10)+=c^48);
	return s^45?r:-r;
}

int main()
{
	int ans=0;
	for(int a1=0;a1<=6;a1++)
	for(int a2=0;a2<=6;a2++)
	for(int a3=0;a3<=6;a3++)
	for(int a4=0;a4<=6;a4++)
	for(int a5=0;a5<=6;a5++)
	{
		if(a1+a2+a3+a4+a5==14) 	
			ans++;
	}
	cout<<ans;
	//1420
	return 0;
}

