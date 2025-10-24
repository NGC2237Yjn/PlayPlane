#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    创建飞机
    在 pygame 中，所有可移动的对象均看作一个精灵（sprite）。
    该类实现了更精确的碰撞检测（mask）并统一边界处理。
"""
import os
import pygame
from config.settings import BASE_DIR


class OurPlane(pygame.sprite.Sprite):
    """我方飞机"""

    # ---------- 1. 常量：底部预留边距 ----------
    MARGIN_BOTTOM = 60          # 之前硬编码的 60 提出常量，避免魔法数字

    def __init__(self, bg_size):
        super(OurPlane, self).__init__()

        self.width, self.height = bg_size      # 背景尺寸

        # ---------- 2. 加载图片：加异常保护 + convert_alpha ----------
        try:
            self.image_one = pygame.image.load(
                os.path.join(BASE_DIR, "material/image/hero1.png")
            ).convert_alpha()
            self.image_two = pygame.image.load(
                os.path.join(BASE_DIR, "material/image/hero2.png")
            ).convert_alpha()
        except pygame.error as e:
            # 素材缺失时直接退出并给出明确提示
            raise SystemExit(f"[ERROR] 飞机图片加载失败: {e}")

        self.rect = self.image_one.get_rect()
        self.mask  = pygame.mask.from_surface(self.image_one)

        # 初始位置：水平居中，底部留边距
        self.rect.left = (self.width - self.rect.width) // 2
        self.rect.top  = self.height - self.rect.height - self.MARGIN_BOTTOM

        self.speed   = 10
        self.active  = True

        # ---------- 3. 爆炸图延迟加载（可选优化） ----------
        self.destroy_images = []
        self._load_destroy_images()

    # ---------- 4. 封装爆炸图加载，同样加保护 ----------
    def _load_destroy_images(self):
        """延迟加载爆炸序列图"""
        names = [f"hero_blowup_n{i}.png" for i in range(1, 5)]
        for name in names:
            try:
                img = pygame.image.load(
                    os.path.join(BASE_DIR, "material/image", name)
                ).convert_alpha()
                self.destroy_images.append(img)
            except pygame.error as e:
                raise SystemExit(f"[ERROR] 爆炸图 {name} 加载失败: {e}")

    # ---------- 5. 移动函数：统一用 min/max 做边界裁剪 ----------
    def move_up(self):
        self.rect.top = max(self.rect.top - self.speed, 0)

    def move_down(self):
        # 下边界 = 背景高 - 预留边距 - 飞机高
        max_top = self.height - self.MARGIN_BOTTOM - self.rect.height
        self.rect.top = min(self.rect.top + self.speed, max_top)

    def move_left(self):
        self.rect.left = max(self.rect.left - self.speed, 0)

    def move_right(self):
        max_left = self.width - self.rect.width
        self.rect.left = min(self.rect.left + self.speed, max_left)

    # ---------- 6. 复活：回到初始位置 + 状态复位 ----------
    def reset(self):
        self.rect.left = (self.width - self.rect.width) // 2
        self.rect.top  = self.height - self.rect.height - self.MARGIN_BOTTOM
        self.active    = True
        # 如果外部有爆炸帧索引，也可在这里重置
        # self.destroy_index = 0
