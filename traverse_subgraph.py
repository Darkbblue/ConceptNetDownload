# 给定中心
# 从中心点开始，遍历所有邻居，根据特定规则过滤掉一部分不符合要求的邻居
# 记录下每个点的出现情况，以及到中心的距离
# 对于尚未出现过的点，将其加入历史记录，并记录下距离，然后继续遍历邻居
# 对于出现过的点，若距离更短，则进行一次距离更新，并在跳过下载的情况下遍历邻居

# 此版本将下载简化为直接以原图中的 @id 为 key 存入一整个 json 文件中
# 由于边下载的触发位置，处于子图边缘处的点不会保存所关联的边，所以我将半径限制增加一，从而确保所要使用的点都是信息完整的

# TODO: 分别实现更合理的边和点的下载，调整过滤器的过滤规则

import requests
import json
from time import sleep

origin = '/c/en/pet' # 所选子图的中心点
size = 2 # 半径限制

result = {}

record_node = {} # 历史记录，key 为点的 @id，value 为当前发现的到中心点的最短距离
record_edge = {} # 历史记录，key 为边的 @id

def get_node(ID):
	'''
	传入URI，返回解析好的词典
	'''
	i = 2 # 重试计数器
	while i < 5:
		try:
			response = requests.get('http://api.conceptnet.io'+ID, timeout=5)
			if response.status_code == 200: # 若正常获取则返回结果
				return response.json()
			else:
				raise requests.exceptions.RequestException
		except requests.exceptions.RequestException:
			print('!reconnecting!')
			sleep(0.1)
			i += 1 # 若出现错误，则进行有限次数重试
	raise 'get failed'

def download_node(node_id):
	'''
	下载点
	'''
	node = get_node(node_id) # 获得点的数据
	result[node_id] = {}
	# 目前阶段只保留下两项数据，并把边列表初始化为空
	result[node_id]['@context'] = node['@context']
	result[node_id]['@id'] = node['@id']
	result[node_id]['edges'] = []

def to_filter(edge, target):
	'''
	根据边的信息判断是否需要进行过滤，若需要过滤 (不记录此点) 则返回 True
	'''
	# 过滤非英文节点
	if 'language' not in edge[target] or edge[target]['language'] != 'en':
		return True
	# 过滤指定关系的边
	if edge['rel']['@id'] in ['/r/Synonym', '/r/Antonym', '/r/RelatedTo', '/r/HasContext', '/r/EtymologicallyRelatedTo',
		'/r/EtymologicallyDerivedFrom', '/r/ExternalURL', '/r/FormOf', '/r/HasContext']:
		return True
	return False

def traverse(start_dist, end):
	'''
	递归地遍历子图，传入激活此点的邻居到中心的距离，以及指定的被激活的端点
	'''
	# 若是尚未记录的点，或者记录过但是这次访问的距离更短，则尝试以此为起点激活所有邻居
	if end not in record_node or (end in record_node and start_dist + 1 < record_node[end]):
		# 若确实尚未记录，则下载此点
		if end not in record_node:
			record_node[end] = start_dist + 1 # 添加记录
			# download (TODO)
			download_node(end)
			if len(record_node) >= 200:
				return
			# 打印辅助信息
			print(record_node[end], end)
			if len(record_node) % 50 == 0:
				print(len(record_node))
		else:
			record_node[end] = start_dist + 1 # 修改记录

		# 若尚未达到半径限制，则以此为起点激活所有邻居
		if start_dist + 1 <= size:
			node = get_node(end)
			has_next_page = True
			while has_next_page:
				for edge in node['edges']:
					# 下载尚未记录的边
					if edge['@id'] not in record_edge:
						record_edge[edge['@id']] = 0
						# download (TODO)
						result[end]['edges'].append(edge) # 将边的信息加入点的记录中
						result[edge['@id']] = edge # 单独保存一份边的信息

					# 递归地访问邻居，只有邻居尚未超出半径限制时才会进行访问
					if start_dist + 1 < size:
						# 确认邻居是来自边的起点还是终点
						if end == edge['end']['@id']:
							next_node = 'start'
						else:
							next_node = 'end'
						# 根据过滤规则若需要继续访问，则递归地进行
						if not to_filter(edge, next_node):
							traverse(record_node[end], edge[next_node]['@id'])

				# 一些实现逐页查看的逻辑，应该不需要修改
				if 'view' in node and 'nextPage' in node['view']:
					node = get_node(node['view']['nextPage'])
				else:
					has_next_page = False


if __name__ == '__main__':
	traverse(-1, origin)

	with open('result.json', 'w') as f:
		f.write(json.dumps(result))

	print('result')
	#print(result)
