#!/usr/bin/python
import sys
import math
import copy

task=0
player="NONE"
opponent="NONE"
cutoff_depth=0
cutoff_player=0
cutoff_opponent=0
algo_player=0
algo_opponent=0
grid_values=[[0 for x in range(5)] for x in range(5)]
initial_state=[['' for x in range(5)] for x in range(5)]
grid_dict={'00':'A1','01':'B1','02':'C1','03':'D1','04':'E1','10':'A2','11':'B2','12':'C2','13':'D2','14':'E2','20':'A3','21':'B3','22':'C3','23':'D3','24':'E3','30':'A4','31':'B4','32':'C4','33':'D4','34':'E4','40':'A5','41':'B5','42':'C5','43':'D5','44':'E5'}
initial_node={}
fp_log=''

def parseInputFile():
	input_file= sys.argv[2]
        fp=open(input_file,'r')
        input_content=fp.read()
	fp.close()
	return input_content

def evaluateState(state,turn):
        playerval=opponentval=0
        for i in range(5):
                for j in range(5):
                        if state[i][j]==turn: playerval+=grid_values[i][j]
                        elif state[i][j]=="*": continue
                        else: opponentval+=grid_values[i][j]
        return playerval-opponentval

def extractParameters():
	input_content=parseInputFile()
	parameters=input_content.split("\n")
	parameters = [x.rstrip() for x in parameters]
	global task,player,opponent,cutoff_depth,grid_values,initial_state,algo_player,algo_opponent,cutoff_player,cutoff_opponent
	task=int(parameters[0])
	player=parameters[1]
	if task==4:
		algo_player=int(parameters[2])
		cutoff_player=int(parameters[3])
		opponent=parameters[4]
		algo_opponent=int(parameters[5])
		cutoff_opponent=int(parameters[6])
		rownum=0
                for value_row in parameters[7:12]:
                        colnum=0
                        for val in value_row.split(" "):
                                grid_values[rownum][colnum]=int(val)
                                colnum+=1
                        rownum+=1
                rownum=0
                for position_row in parameters[12:17]:
                        colnum=0
                        for position in position_row:
                                initial_state[rownum][colnum]=position
                                colnum+=1
                        rownum+=1
                initial_node['state']=initial_state
                initial_node['parent']=''
                initial_node['depth']=0
                initial_node['eval']=float("-inf")
                initial_node['square']='root'	
	else:
 		if player=="X":
			opponent="O"
		else :  opponent="X"
		cutoff_depth=int(parameters[2])
		rownum=0
		for value_row in parameters[3:8]:
			colnum=0
			for val in value_row.split(" "):
				grid_values[rownum][colnum]=int(val)
				colnum+=1
			rownum+=1
		rownum=0
		for position_row in parameters[8:13]:
                        colnum=0
                        for position in position_row:
                               	initial_state[rownum][colnum]=position
                                colnum+=1
                        rownum+=1
		initial_node['state']=initial_state
        	initial_node['parent']=''
        	initial_node['depth']=0
        	initial_node['eval']=float("-inf")
        	initial_node['square']='root'


def isGoalState(state):
	for i in range(5):
		for j in range(5):
			if state[i][j]=="*": return False;
	return True;

def hasAdjacentPlayer(new_state,i,j,turn):
	if i==0:
		if j==0:
			if new_state[i][j+1]==turn or new_state[i+1][j]==turn: return True;
		elif j==4:
			if new_state[i][j-1]==turn or new_state[i+1][j]==turn: return True;
		elif new_state[i][j+1]==turn or new_state[i][j-1]==turn or new_state[i+1][j]==turn: return True;
	elif i==4:
		if j==0:
			if new_state[i][j+1]==turn or new_state[i-1][j]==turn: return True;
		elif j==4:
			if new_state[i][j-1]==turn or new_state[i-1][j]==turn: return True;		
		elif new_state[i][j+1]==turn or new_state[i][j-1]==turn or new_state[i-1][j]==turn: return True;
	elif j==0:
		if new_state[i][j+1]==turn or new_state[i-1][j]==turn or new_state[i+1][j]==turn: return True;		
	elif j==4:
		if new_state[i-1][j]==turn or new_state[i][j-1]==turn or new_state[i+1][j]==turn: return True;
	else:
		if new_state[i][j+1]==turn or new_state[i][j-1]==turn or new_state[i+1][j]==turn or new_state[i-1][j]==turn: return True;
	return False;

def attemptRaid(new_state,i,j,turn):
	oppo=opponent
	if turn==opponent:
		oppo=player
	if (hasAdjacentPlayer(new_state,i,j,turn)==True):
		if i==0:           
                	if j==0:
                        	if new_state[i][j+1]==oppo: new_state[i][j+1]=turn
				if new_state[i+1][j]==oppo: new_state[i+1][j]=turn
               		elif j==4:
                        	if new_state[i][j-1]==oppo: new_state[i][j-1]=turn

				if new_state[i+1][j]==oppo: new_state[i+1][j]=turn
                	else:
				if new_state[i][j+1]==oppo: new_state[i][j+1]=turn
				if new_state[i][j-1]==oppo: new_state[i][j-1]=turn
				if new_state[i+1][j]==oppo: new_state[i+1][j]=turn
        	elif i==4:
                	if j==0:
                        	if new_state[i][j+1]==oppo: new_state[i][j+1]=turn
				if new_state[i-1][j]==oppo: new_state[i-1][j]=turn
                	elif j==4:
                        	if new_state[i][j-1]==oppo: new_state[i][j-1]=turn
				if new_state[i-1][j]==oppo: new_state[i][j-1]=turn 
                	else:	
				if new_state[i][j+1]==oppo: new_state[i][j+1]=turn
				if new_state[i][j-1]==oppo: new_state[i][j-1]=turn
				if new_state[i-1][j]==oppo: new_state[i-1][j]=turn
        	elif j==0:
                	if new_state[i][j+1]==oppo: new_state[i][j+1]=turn
			if new_state[i-1][j]==oppo: new_state[i-1][j]=turn
			if new_state[i+1][j]==oppo: new_state[i+1][j]=turn
        	elif j==4:
                	if new_state[i-1][j]==oppo: new_state[i-1][j]=turn
			if new_state[i][j-1]==oppo: new_state[i][j-1]=turn
			if new_state[i+1][j]==oppo: new_state[i+1][j]=turn
        	else:
                	if new_state[i][j+1]==oppo: new_state[i][j+1]=turn
			if new_state[i][j-1]==oppo: new_state[i][j-1]=turn
			if new_state[i+1][j]==oppo: new_state[i+1][j]=turn
			if new_state[i-1][j]==oppo: new_state[i-1][j]=turn
	return new_state

def updateFrontierGBFS(frontier,node,turn,depth):
	state=node['state']
	if(isGoalState(state)):
		return
	else:
		for i in range(5):
			for j in range(5):
				if(state[i][j]=="*"):
					newnode={}
					new_state=[['' for x in range(5)] for x in range(5)]
					for x in range(5):
						for y in range(5):
							new_state[x][y]=state[x][y]
					new_state[i][j]=turn
					new_state=attemptRaid(new_state,i,j,turn)
					newnode['square']=grid_dict[str(i)+str(j)]
					newnode['parent']=node
					newnode['depth']=node['depth']+1
					newnode['eval']=evaluateState(new_state,turn)
					newnode['state']=new_state
					frontier.append(newnode)

def findMaxValueStateGBFS(frontier):
	maxlevel=0
	for node in frontier:
		if node['depth']>maxlevel:
			maxlevel=node['depth']
	level=[]
	for node in frontier:
		if node['depth']==maxlevel:
			level.append(node)
	maxval=level[0]['eval']
	maxindex=0
	for node in level[1:]:
		if maxval<node['eval']:
			maxval=node['eval']
			maxindex=level.index(node)
	maxnode=level[maxindex]
	return maxnode
	
def greedyBFS(frontier,node,depth,turn):
	updateFrontierGBFS(frontier,node,turn,1)
	return findMaxValueStateGBFS(frontier)

def writeToLog(node,depth):
	global fp_log
	if node['depth']==depth:
		if node['eval']==float("inf"):
			fp_log.write("%s,%d,Infinity\r\n"%(node['square'],node['depth']))	
		elif node['eval']==float("-inf"):
			fp_log.write("%s,%d,-Infinity\r\n"%(node['square'],node['depth']))
		else:
			if node['depth']%2==0:
				fp_log.write("%s,%d,%d\r\n"%(node['square'],node['depth'],-int(node['eval'])))
			else:
				fp_log.write("%s,%d,%d\r\n"%(node['square'],node['depth'],int(node['eval'])))
	if (node['parent'])['eval']!=float("-inf"):
		newnode=node['parent']
		if node['depth']%2==0:
                       	fp_log.write("%s,%d,%d\r\n"%(newnode['square'],newnode['depth'],-int(newnode['eval'])))
                else:
                        fp_log.write("%s,%d,%d\r\n"%(newnode['square'],newnode['depth'],int(newnode['eval'])))

def updateFrontierminimax(frontier,node,turn,depth):
	state=node['state']
	global fp_log
        if(isGoalState(state)):
               	return
        else:
                for i in range(5):
                        for j in range(5):
                                if(state[i][j]=="*"):
                                        newnode={}
                                        new_state=[['' for x in range(5)] for x in range(5)]
                                        for x in range(5):
                                        	for y in range(5):
                                                	new_state[x][y]=state[x][y]
                                        new_state[i][j]=turn
                                        new_state=attemptRaid(new_state,i,j,turn)
                                        newnode['square']=grid_dict[str(i)+str(j)]
                                        newnode['parent']=node
                                        newnode['depth']=(node['depth']+1)%(depth+1)
					if depth==newnode['depth']:
                                        	newnode['eval']=evaluateState(new_state,turn)
                                        else:
						if newnode['depth']%2==0:
							newnode['eval']=float("-inf")
						else:
							newnode['eval']=float("inf")
							if task!=4:
								if (newnode['parent'])['square']!='root':
									writeToLog(newnode,depth)	
								else:
									fp_log.write("%s,1,Infinity\r\n"%newnode['square'])
					newnode['state']=new_state
					newnode_copy=copy.deepcopy(newnode)
					if depth!=newnode['depth']:
						if turn==player:
							updateFrontierminimax(frontier,newnode_copy,opponent,depth)
						else:
							updateFrontierminimax(frontier,newnode_copy,player,depth)
					newnode=copy.deepcopy(newnode_copy)
					if node['eval']==float("inf") or node['eval']==float("-inf"):
						if node['depth']!=depth-1:
							node['eval']=-newnode['eval']
						else:
							node['eval']=newnode['eval']
						newnode['parent']=node
					else:
						if node['depth']!=depth-1:
							if -newnode['eval']>node['eval']:
								node['eval']=-newnode['eval']
								newnode['parent']=node
						else:
							if newnode['eval']>node['eval']:	
								node['eval']=newnode['eval']
								newnode['parent']=node
							
					if task!=4:
                                        	writeToLog(newnode,depth)
					frontier.append(newnode)	

def nextStateMinimax(frontier,node,depth):
	for elem in frontier:
		if elem['depth']==1:
			if elem['parent']==node:
				if depth<2:
					if elem['eval']==node['eval']:
						return elem
				else:
					if -elem['eval']==node['eval']:
						return elem
	return "null" 

def miniMax(frontier,node,depth,turn):
	node['depth']=0
	node['parent']=''
	node['eval']=float("-inf")
	global fp_log
	if task!=4:
		fp_log=open("traverse_log.txt","w")
		fp_log.close()
		fp_log=open("traverse_log.txt","a")
		fp_log.write("Node,Depth,Value\r\n")
		fp_log.write("root,0,-Infinity\r\n")
	updateFrontierminimax(frontier,node,turn,depth)
        if task!=4:
		fp_log.seek(-2,1)
       	 	fp_log.truncate()
		fp_log.close()
	return nextStateMinimax(frontier,node,depth)

def formatInfinity(value):
	if value==float("-inf"): return "-Infinity"
	elif value==float("inf"): return "Infinity"
	else: return str(value)

def nextStateAlphaBeta(frontier,node):
        for elem in frontier:
                if elem['depth']==1:
                        if elem['parent']==node:
                                if elem['eval']==node['eval']:
                                        return elem
        return "null"

def writeToLogAlphaBeta(node,depth,alpha,beta,old_alpha,old_beta):
        global fp_log
        if node['depth']==depth:
                if node['eval']==float("inf"):
                        fp_log.write("%s,%d,Infinity,%s,%s\r\n"%(node['square'],node['depth'],formatInfinity(old_alpha),formatInfinity(old_beta)))
                elif node['eval']==float("-inf"):
                        fp_log.write("%s,%d,-Infinity,%s,%s\r\n"%(node['square'],node['depth'],formatInfinity(old_alpha),formatInfinity(old_beta)))
                else:
                        if node['depth']%2==0:
                                fp_log.write("%s,%d,%d,%s,%s\r\n"%(node['square'],node['depth'],-int(node['eval']),formatInfinity(old_alpha),formatInfinity(old_beta)))
                        else:
                                fp_log.write("%s,%d,%d,%s,%s\r\n"%(node['square'],node['depth'],int(node['eval']),formatInfinity(old_alpha),formatInfinity(old_beta)))
        if (node['parent'])['eval']!=float("-inf"):
               newnode=node['parent'] 
	       if node['depth']%2==0:
                        fp_log.write("%s,%d,%d,%s,%s\r\n"%(newnode['square'],newnode['depth'],-int(newnode['eval']),formatInfinity(alpha),formatInfinity(beta)))
               else:
                        fp_log.write("%s,%d,%d,%s,%s\r\n"%(newnode['square'],newnode['depth'],int(newnode['eval']),formatInfinity(alpha),formatInfinity(beta)))

def updateFrontierAlphaBeta(frontier,node,turn,depth,alpha,beta):
        state=node['state']
	prune=False
        global fp_log
        if(isGoalState(state)):
                return
        else:
                for i in range(5):
                        for j in range(5):
                                if(state[i][j]=="*"):
                                        newnode={}
                                        new_state=[['' for x in range(5)] for x in range(5)]
                                        for x in range(5):
                                                for y in range(5):
                                                        new_state[x][y]=state[x][y]
                                        new_state[i][j]=turn
                                        new_state=attemptRaid(new_state,i,j,turn)
                                        newnode['square']=grid_dict[str(i)+str(j)]
                                        newnode['parent']=node
                                        newnode['depth']=(node['depth']+1)%(depth+1)
                                        if depth==newnode['depth']:
                                                newnode['eval']=evaluateState(new_state,turn)
                                        else:
                                                if newnode['depth']%2==0:
                                                        newnode['eval']=float("-inf")
                                                else:
                                                        newnode['eval']=float("inf")
                                                        if task!=4:
                                                                if (newnode['parent'])['square']!='root':
                                                                        writeToLogAlphaBeta(newnode,depth,alpha,beta,alpha,beta)
                                                                else:
                                                                        fp_log.write("%s,1,Infinity,%s,%s\r\n"%(newnode['square'],formatInfinity(alpha),formatInfinity(beta)))
					newnode['state']=new_state
                                        newnode_copy=copy.deepcopy(newnode)
                                        if depth!=newnode['depth']:
                                                if turn==player:
                                                        updateFrontierAlphaBeta(frontier,newnode_copy,opponent,depth,alpha,beta)
                                                else:
                                                        updateFrontierAlphaBeta(frontier,newnode_copy,player,depth,alpha,beta)
                                        newnode=copy.deepcopy(newnode_copy)
                                        old_alpha=alpha
                                        old_beta=beta
					if node['eval']==float("inf") or node['eval']==float("-inf"):
                                                if node['depth']!=depth-1:
                                                        node['eval']=-newnode['eval']
                                                else:
                                                        node['eval']=newnode['eval']
                                                newnode['parent']=node
                                        else:
                                                if node['depth']!=depth-1:
                                                        if -newnode['eval']>node['eval']:
                                                                node['eval']=-newnode['eval']
                                                                newnode['parent']=node
                                                else:
                                                        if newnode['eval']>node['eval']:
                                                                node['eval']=newnode['eval']
                                                                newnode['parent']=node

                                        if node['depth']%2==1:
                                                beta=min(beta,-newnode['eval'])
                                                if beta<=alpha:
                                                        writeToLogAlphaBeta(newnode,depth,alpha,old_beta,old_alpha,old_beta)
                                                        prune=True
                                                        break
                                        else:
						if newnode['depth']!=depth:
							alpha=max(alpha,-newnode['eval'])
						else:
                                                	alpha=max(alpha,newnode['eval'])
                                                if beta<=alpha:
                                                        writeToLogAlphaBeta(newnode,depth,old_alpha,beta,old_alpha,old_beta)
                                                        prune=True
                                                        break
                                        if task!=4:
                                                writeToLogAlphaBeta(newnode,depth,alpha,beta,old_alpha,old_beta)
                                        frontier.append(newnode)
                        if prune==True:
                                break

def alphaBetaPruning(frontier,node,depth,turn):
	node['depth']=0
        node['parent']=''
        node['eval']=float("-inf")
        global fp_log
	alpha=float("-inf")
	beta=float("inf")
       	if task!=4:
                fp_log=open("traverse_log.txt","w")
                fp_log.close()
                fp_log=open("traverse_log.txt","a")
                fp_log.write("Node,Depth,Value,Alpha,Beta\r\n")
                fp_log.write("root,0,-Infinity,-Infinity,Infinity\r\n")
        updateFrontierAlphaBeta(frontier,node,turn,depth,alpha,beta)
       	if task!=4:	
		fp_log.seek(-2,1)
        	fp_log.truncate()
        	fp_log.close()
        return nextStateMinimax(frontier,node,depth)

def writeNextState(node):
	nextState=node['state']
	fp=open("next_state.txt","w");
	for i in range(5):
		for j in range(5):
			fp.write(nextState[i][j])
		if i<4 : fp.write("\r\n")
	fp.close()

if __name__ == "__main__":
	extractParameters()
	algo={1:greedyBFS,2:miniMax,3:alphaBetaPruning}
	if task!=4:
		frontier=[]
        	frontier.append(initial_node)
		nextState=algo[int(task)](frontier,initial_node,cutoff_depth,player)
		writeNextState(nextState)
	else:
		turn=player
		node=initial_node
		frontierPlayer=[]
		frontierPlayer.append(initial_node)
		frontierOpp=[]
		fp=open("trace_state.txt","w")
		fp.close()
		fp=open("trace_state.txt","a")
		while isGoalState(node['state'])==False:
			if turn==player:
				node=algo[algo_player](frontierPlayer,node,cutoff_player,turn)
				turn=opponent
				state=node['state']
				del frontierPlayer[:]
				frontierPlayer.append(node)
				for i in range(5):
					fp.write("%s\r\n"%''.join(state[i]))
			else:
				if len(frontierOpp)==0:
					frontierOpp.append(node)
				node=algo[algo_opponent](frontierOpp,node,cutoff_opponent,turn)     
				turn=player	
				state=node['state']
				del frontierOpp[:]
				frontierOpp.append(node)
                                for i in range(5):
                                       fp.write("%s\r\n"%''.join(state[i]))
		fp.seek(-2,1)
		fp.truncate()
		fp.close()

